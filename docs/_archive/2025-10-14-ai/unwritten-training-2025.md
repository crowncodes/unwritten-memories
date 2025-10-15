# Unwritten Ultra-Lightweight Model Training Guide (2025 Edition)
## Complete Step-by-Step Implementation with Latest Techniques

**Goal**: Create a 2-3MB multi-task model for on-device AI in your card game  
**Target Performance**: 8-15ms inference, <10% battery drain per 30min session  
**Updated**: October 2025 with latest frameworks and techniques

---

## What's New in 2025

### Major Framework Updates
- **LiteRT** (formerly TensorFlow Lite) - New name, better PyTorch support via AI Edge Torch
- **PyTorch 2.5+** with `torch.compile` for 1.5-2x training speedup
- **Advanced Quantization**: INT4, INT2 support with QAT/QAD (Quantization-Aware Distillation)
- **Multi-Task LoRA**: MTL-LoRA, LoRI, MoRE for efficient parameter sharing
- **Gemma 3 270M** reference: Google's ultra-efficient 270M parameter model achieving 0.75% battery for 25 conversations

### Key Improvements Over 2024 Approach
- LoRA/PEFT instead of full fine-tuning (95% fewer trainable parameters)
- Quantization-aware training from the start (not post-training)
- PyTorch 2.x compile optimizations (40%+ faster training)
- Better synthetic data generation with latest LLMs
- Direct PyTorch → LiteRT conversion with AI Edge Torch

---

## Phase 1: Environment Setup (Day 1-2)

### 1.1 Development Environment

```bash
# Create virtual environment
python3.11 -m venv unwritten-env
source unwritten-env/bin/activate  # Linux/Mac
# unwritten-env\Scripts\activate  # Windows

# Core dependencies - PyTorch 2.5+
pip install torch==2.5.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install transformers==4.45.0
pip install datasets==3.0.0
pip install peft==0.13.0  # Parameter-Efficient Fine-Tuning
pip install bitsandbytes==0.44.0  # For 4-bit quantization

# Data and tracking
pip install pandas scikit-learn tqdm wandb accelerate

# Model conversion and deployment
pip install ai-edge-torch  # New PyTorch → LiteRT converter
pip install ai-edge-quantizer  # For optimal quantization
```

### 1.2 Hardware Requirements

**Minimum for Training:**
- GPU: 12GB VRAM (RTX 3060/4060 Ti recommended) - LoRA reduces requirements
- RAM: 16GB
- Storage: 50GB free space
- Training time: 1-2 days (much faster with LoRA)

**Cloud Alternative (Recommended):**
- Google Colab Pro ($12/month) - A100 available
- Lambda Labs GPU Cloud ($0.80/hr for A100)
- Paperspace Gradient

---

## Phase 2: Data Collection & Preparation (Day 3-7)

### 2.1 Data Requirements (Reduced with LoRA)

| Task | Minimum with LoRA | Ideal | Format |
|------|-------------------|-------|---------|
| **Personality Traits** | 3,000 examples | 10,000+ | Text → 5 trait scores |
| **Sentiment Analysis** | 2,000 examples | 8,000+ | Text → Emotion label |
| **Text Generation** | 5,000 examples | 15,000+ | Context → Response |
| **Relationship Scoring** | 1,000 examples | 5,000+ | Interaction → Score |

**Total minimum**: ~12,000 examples (LoRA allows smaller datasets)  
**Total ideal**: ~40,000 examples

### 2.2 Modern Synthetic Data Generation

```python
import anthropic
import json
from tqdm import tqdm

def generate_training_data_claude(seed_examples, target_count=5000):
    """
    Use Claude 3.5 Sonnet for high-quality synthetic data
    More cost-effective and better quality than GPT-4 for this use case
    """
    client = anthropic.Anthropic(api_key="your-api-key")
    synthetic_data = []
    
    # Create few-shot examples
    prompt_examples = "\n".join([
        f"Text: {ex['text']}\nTraits: {json.dumps(ex['traits'])}"
        for ex in seed_examples[:5]
    ])
    
    batch_size = 20  # Generate multiple at once
    num_batches = target_count // batch_size
    
    for batch in tqdm(range(num_batches)):
        prompt = f"""Generate {batch_size} NEW card game interaction dialogues with personality traits.

Examples:
{prompt_examples}

Generate {batch_size} diverse examples following this pattern:
1. Unique card interaction dialogues (15-30 words each)
2. Personality trait scores (0.0-1.0) for: openness, conscientiousness, extraversion, agreeableness, neuroticism
3. Cover different emotions, situations, card types

Return as JSON array:
[
  {{"text": "...", "traits": {{"openness": 0.x, ...}}}},
  ...
]"""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            temperature=0.9,
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            batch_data = json.loads(message.content[0].text)
            synthetic_data.extend(batch_data)
        except:
            continue
        
        # Save periodically
        if (batch + 1) % 10 == 0:
            with open(f'synthetic_data_{batch+1}.json', 'w') as f:
                json.dump(synthetic_data, f)
    
    return synthetic_data

# Cost: ~$30-40 for 40K examples with Claude 3.5 Sonnet
personality_data = generate_training_data_claude(seed_personality, 10000)
```

### 2.3 Data Validation and Quality Control

```python
from datasets import Dataset, DatasetDict

class DataValidator:
    """Ensure data quality before training"""
    
    def validate_and_clean(self, examples, task_type):
        """Validate and clean examples for a specific task"""
        valid = []
        
        for ex in examples:
            if task_type == 'personality':
                if (ex.get('text') and 
                    len(ex['text'].split()) >= 10 and
                    all(0 <= ex['traits'].get(t, -1) <= 1 
                        for t in ['openness', 'conscientiousness', 
                                 'extraversion', 'agreeableness', 'neuroticism'])):
                    valid.append(ex)
            elif task_type == 'sentiment':
                if (ex.get('text') and 
                    ex.get('label') in ['positive', 'negative', 'neutral']):
                    valid.append(ex)
            # Add other task validations...
        
        print(f"{task_type}: {len(valid)}/{len(examples)} valid examples")
        return valid

# Create Hugging Face datasets
validator = DataValidator()

dataset_dict = DatasetDict({
    'personality': Dataset.from_list(
        validator.validate_and_clean(personality_data, 'personality')
    ),
    'sentiment': Dataset.from_list(
        validator.validate_and_clean(sentiment_data, 'sentiment')
    ),
    # ... other tasks
})

# Split data
dataset_dict = dataset_dict.train_test_split(test_size=0.2)
```

---

## Phase 3: Model Architecture with LoRA (Day 8-10)

### 3.1 Base Model Selection

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from peft import LoraConfig, get_peft_model, TaskType
import torch
import torch.nn as nn

# Use a small, efficient base model
BASE_MODEL = "google/gemma-2-2b"  # Or "microsoft/phi-2" (2.7B)

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
```

### 3.2 Multi-Task Model with MTL-LoRA

```python
class MultiTaskLoRAModel(nn.Module):
    """
    Multi-task model using LoRI approach for reduced cross-task interference
    Based on: https://arxiv.org/abs/2504.07448
    """
    
    def __init__(self, base_model_name, num_tasks=4):
        super().__init__()
        
        # Load base model (frozen)
        from transformers import AutoModel
        self.base_model = AutoModel.from_pretrained(
            base_model_name,
            torch_dtype=torch.float16  # Memory efficient
        )
        
        # Freeze base model
        for param in self.base_model.parameters():
            param.requires_grad = False
        
        hidden_size = self.base_model.config.hidden_size
        
        # Task-specific LoRA configurations
        # Using different ranks for different tasks (MoRE approach)
        self.task_configs = {
            'personality': {
                'r': 8,  # Rank
                'lora_alpha': 16,
                'target_modules': ["q_proj", "v_proj"],
                'lora_dropout': 0.1
            },
            'sentiment': {
                'r': 4,
                'lora_alpha': 8,
                'target_modules': ["q_proj", "v_proj"],
                'lora_dropout': 0.1
            },
            'dialogue': {
                'r': 16,
                'lora_alpha': 32,
                'target_modules': ["q_proj", "v_proj", "k_proj"],
                'lora_dropout': 0.1
            },
            'relationship': {
                'r': 4,
                'lora_alpha': 8,
                'target_modules': ["q_proj", "v_proj"],
                'lora_dropout': 0.1
            }
        }
        
        # Task-specific heads (lightweight)
        self.personality_head = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(64, 5)  # 5 personality traits
        )
        
        self.sentiment_head = nn.Sequential(
            nn.Linear(hidden_size, 32),
            nn.GELU(),
            nn.Linear(32, 3)  # 3 sentiment classes
        )
        
        self.dialogue_head = nn.Linear(hidden_size, hidden_size)
        
        self.relationship_head = nn.Sequential(
            nn.Linear(hidden_size, 32),
            nn.GELU(),
            nn.Linear(32, 1)
        )
    
    def forward(self, input_ids, attention_mask, task):
        """Forward pass for specific task"""
        outputs = self.base_model(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        
        # Use CLS token
        hidden = outputs.last_hidden_state[:, 0, :]
        
        if task == 'personality':
            return torch.sigmoid(self.personality_head(hidden))
        elif task == 'sentiment':
            return self.sentiment_head(hidden)
        elif task == 'dialogue':
            return self.dialogue_head(hidden)
        elif task == 'relationship':
            return torch.sigmoid(self.relationship_head(hidden))

# Initialize model
model = MultiTaskLoRAModel(BASE_MODEL)

# Apply LoRA using PEFT
from peft import get_peft_model, LoraConfig

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.FEATURE_EXTRACTION
)

model = get_peft_model(model.base_model, lora_config)

# Count parameters
trainable, total = model.get_nb_trainable_parameters()
print(f"Trainable: {trainable:,} ({100*trainable/total:.2f}%)")
print(f"Total: {total:,}")
# Expected: ~0.5-2% of parameters trainable with LoRA
```

---

## Phase 4: Training with Modern Optimizations (Day 11-18)

### 4.1 Setup Training with PyTorch 2.x Optimizations

```python
from transformers import Trainer, TrainingArguments
from torch.optim import AdamW
import torch

# Enable PyTorch 2.x compile for 40%+ speedup
if hasattr(torch, 'compile'):
    model = torch.compile(model, mode='max-autotune')

# Training arguments optimized for 2025
training_args = TrainingArguments(
    output_dir="./unwritten-checkpoints",
    num_train_epochs=10,
    per_device_train_batch_size=32,  # Larger with LoRA
    per_device_eval_batch_size=64,
    learning_rate=5e-4,  # Higher LR for LoRA
    warmup_steps=500,
    weight_decay=0.01,
    logging_steps=50,
    evaluation_strategy="steps",
    eval_steps=500,
    save_steps=1000,
    save_total_limit=3,
    
    # Modern optimizations
    bf16=True,  # Use BF16 on modern GPUs (A100, H100, RTX 40-series)
    gradient_checkpointing=True,  # Save memory
    optim="adamw_torch_fused",  # Faster optimizer (PyTorch 2.x)
    torch_compile=True,  # Enable compilation
    dataloader_num_workers=4,
    dataloader_pin_memory=True,
    
    # Distributed training (if available)
    ddp_find_unused_parameters=False,
    
    report_to="wandb",  # Track experiments
)

# Advanced: 4-bit quantization during training (QLoRA)
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,  # Nested quantization
)
```

### 4.2 Quantization-Aware Training (QAT)

```python
class QATTrainer:
    """
    Quantization-Aware Training with knowledge distillation
    Based on latest research: https://arxiv.org/abs/2403.11106
    """
    
    def __init__(self, student_model, teacher_model, tokenizer):
        self.student = student_model
        self.teacher = teacher_model
        self.tokenizer = tokenizer
        
        # Prepare student for quantization
        from torch.quantization import prepare_qat, get_default_qat_qconfig
        
        # Configure quantization
        self.student.qconfig = get_default_qat_qconfig('fbgemm')
        self.student = prepare_qat(self.student, inplace=True)
        
        # Optimizer for student only
        self.optimizer = AdamW(
            self.student.parameters(),
            lr=5e-4,
            weight_decay=0.01
        )
        
        # Scheduler
        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer, T_max=10
        )
    
    def distillation_loss(self, student_logits, teacher_logits, 
                         labels=None, temperature=3.0, alpha=0.7):
        """
        Combined KD + QAT loss
        """
        # Soft targets
        soft_loss = nn.KLDivLoss(reduction='batchmean')(
            nn.functional.log_softmax(student_logits / temperature, dim=-1),
            nn.functional.softmax(teacher_logits / temperature, dim=-1)
        ) * (temperature ** 2)
        
        # Hard targets
        if labels is not None:
            hard_loss = nn.CrossEntropyLoss()(student_logits, labels)
            return alpha * soft_loss + (1 - alpha) * hard_loss
        
        return soft_loss
    
    def train_epoch(self, dataloader, epoch):
        """Train one epoch with QAT"""
        self.student.train()
        self.teacher.eval()
        
        total_loss = 0
        for batch in tqdm(dataloader, desc=f"Epoch {epoch}"):
            input_ids = batch['input_ids'].cuda()
            attention_mask = batch['attention_mask'].cuda()
            labels = batch['labels'].cuda()
            
            # Get teacher predictions (no grad)
            with torch.no_grad():
                teacher_outputs = self.teacher(input_ids, attention_mask)
            
            # Get student predictions
            student_outputs = self.student(input_ids, attention_mask)
            
            # Compute loss
            loss = self.distillation_loss(
                student_outputs,
                teacher_outputs,
                labels
            )
            
            # Backward
            self.optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.student.parameters(), 1.0)
            self.optimizer.step()
            
            total_loss += loss.item()
        
        self.scheduler.step()
        return total_loss / len(dataloader)
```

### 4.3 Multi-Task Training Loop

```python
from torch.utils.data import Dataset, DataLoader
import random

class MultiTaskDataset(Dataset):
    """Dataset that samples from multiple tasks"""
    
    def __init__(self, task_datasets, tokenizer, max_length=128):
        self.task_datasets = task_datasets
        self.tokenizer = tokenizer
        self.max_length = max_length
        
        # Calculate sampling probabilities (proportional to dataset size)
        self.task_names = list(task_datasets.keys())
        sizes = [len(ds) for ds in task_datasets.values()]
        total = sum(sizes)
        self.task_probs = [s/total for s in sizes]
    
    def __len__(self):
        return sum(len(ds) for ds in self.task_datasets.values())
    
    def __getitem__(self, idx):
        # Sample a task
        task = random.choices(self.task_names, weights=self.task_probs)[0]
        
        # Sample from that task
        task_dataset = self.task_datasets[task]
        task_idx = random.randint(0, len(task_dataset) - 1)
        example = task_dataset[task_idx]
        
        # Tokenize
        encoding = self.tokenizer(
            example['text'],
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'task': task,
            'labels': example.get('labels', None)
        }

# Create dataloaders
train_dataset = MultiTaskDataset(
    {
        'personality': dataset_dict['personality']['train'],
        'sentiment': dataset_dict['sentiment']['train'],
        # ... other tasks
    },
    tokenizer
)

train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4,
    pin_memory=True
)

# Training loop with all optimizations
def train_multi_task(model, train_loader, epochs=10):
    """Optimized training loop"""
    
    optimizer = AdamW(model.parameters(), lr=5e-4, fused=True)  # Fused optimizer
    scaler = torch.cuda.amp.GradScaler()  # Mixed precision
    
    # Compile for speed
    if hasattr(torch, 'compile'):
        model = torch.compile(model, mode='reduce-overhead')
    
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        
        for batch in tqdm(train_loader, desc=f"Epoch {epoch+1}"):
            input_ids = batch['input_ids'].cuda()
            attention_mask = batch['attention_mask'].cuda()
            task = batch['task'][0]  # All same task in batch
            
            # Mixed precision training
            with torch.cuda.amp.autocast():
                outputs = model(input_ids, attention_mask, task)
                loss = compute_task_loss(outputs, batch, task)
            
            # Scaled backward
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            scaler.step(optimizer)
            scaler.update()
            optimizer.zero_grad()
            
            total_loss += loss.item()
        
        print(f"Epoch {epoch+1} Loss: {total_loss/len(train_loader):.4f}")

train_multi_task(model, train_loader)
```

---

## Phase 5: Model Conversion & Compression (Day 19-21)

### 5.1 PyTorch to LiteRT Conversion

```python
import ai_edge_torch
import torch

def convert_to_litert(pytorch_model, sample_inputs):
    """
    Convert PyTorch model to LiteRT format
    Using new AI Edge Torch converter (2025)
    """
    
    # Export to edge format
    edge_model = ai_edge_torch.convert(
        pytorch_model.eval(),
        sample_inputs
    )
    
    # Save as .tflite
    edge_model.export("unwritten_model.tflite")
    
    return edge_model

# Prepare sample inputs
sample_input = torch.randint(
    0, tokenizer.vocab_size, 
    (1, 128)
).cuda()

# Convert
litert_model = convert_to_litert(model, (sample_input,))
```

### 5.2 Advanced Quantization with AI Edge Quantizer

```python
from ai_edge_quantizer import quantize

def quantize_to_int4(tflite_path, output_path):
    """
    Apply INT4 quantization for maximum compression
    Target: 2-3MB final size
    """
    
    # Configure INT4 quantization
    quantization_config = {
        'algorithm': 'int4',
        'granularity': 'per_channel',
        'optimization_strategy': 'accuracy'  # or 'size' for maximum compression
    }
    
    # Quantize
    quantized_model = quantize(
        tflite_path,
        output_path=output_path,
        **quantization_config
    )
    
    # Check size
    import os
    size_mb = os.path.getsize(output_path) / 1024 / 1024
    print(f"✓ Quantized model size: {size_mb:.2f}MB")
    
    return quantized_model

# Apply quantization
quantized_model = quantize_to_int4(
    "unwritten_model.tflite",
    "unwritten_model_int4.tflite"
)
```

### 5.3 Alternative: ONNX with Quantization

```python
import onnx
from onnxruntime.quantization import quantize_dynamic, QuantType

def export_to_onnx_quantized(model, sample_input, output_path):
    """
    Alternative path: ONNX format with quantization
    Good for cross-platform deployment
    """
    
    # Export to ONNX
    torch.onnx.export(
        model,
        sample_input,
        "unwritten_model.onnx",
        input_names=['input_ids'],
        output_names=['personality', 'sentiment', 'dialogue', 'relationship'],
        dynamic_axes={
            'input_ids': {0: 'batch_size', 1: 'sequence'}
        },
        opset_version=17
    )
    
    # Quantize ONNX model
    quantize_dynamic(
        "unwritten_model.onnx",
        output_path,
        weight_type=QuantType.QUInt8
    )
    
    # Verify size
    import os
    size_mb = os.path.getsize(output_path) / 1024 / 1024
    print(f"ONNX quantized size: {size_mb:.2f}MB")
```

---

## Phase 6: Flutter Integration (Day 22-25)

### 6.1 Flutter Setup with LiteRT

```yaml
# pubspec.yaml
dependencies:
  flutter:
    sdk: flutter
  tflite_flutter: ^0.10.4  # Latest version
  
assets:
  - assets/unwritten_model_int4.tflite
```

### 6.2 Flutter Implementation

```dart
// lib/model_service.dart
import 'package:tflite_flutter/tflite_flutter.dart';

class UnwrittenAI {
  late Interpreter _interpreter;
  bool _isInitialized = false;
  
  Future<void> initialize() async {
    try {
      // Load model
      _interpreter = await Interpreter.fromAsset(
        'assets/unwritten_model_int4.tflite',
        options: InterpreterOptions()
          ..threads = 4  // Multi-threading
          ..useNnapi = true  // Use Android NNAPI if available
      );
      
      _isInitialized = true;
      print('✓ Model loaded successfully');
      
      // Print input/output details
      print('Input shape: ${_interpreter.getInputTensors()}');
      print('Output shape: ${_interpreter.getOutputTensors()}');
    } catch (e) {
      print('Error loading model: $e');
    }
  }
  
  Future<Map<String, dynamic>> analyzeInteraction(String text) async {
    if (!_isInitialized) {
      throw Exception('Model not initialized');
    }
    
    // Tokenize input (simplified - use proper tokenizer)
    final input = _tokenize(text, maxLength: 128);
    
    // Prepare outputs
    var personalityOutput = List.filled(5, 0.0).reshape([1, 5]);
    var sentimentOutput = List.filled(3, 0.0).reshape([1, 3]);
    var relationshipOutput = List.filled(1, 0.0).reshape([1, 1]);
    
    // Run inference
    final stopwatch = Stopwatch()..start();
    
    _interpreter.runForMultipleInputs(
      [input],
      {
        0: personalityOutput,  // Personality traits
        1: sentimentOutput,     // Sentiment
        2: relationshipOutput,  // Relationship score
      }
    );
    
    stopwatch.stop();
    print('Inference time: ${stopwatch.elapsedMilliseconds}ms');
    
    return {
      'personality': {
        'openness': personalityOutput[0][0],
        'conscientiousness': personalityOutput[0][1],
        'extraversion': personalityOutput[0][2],
        'agreeableness': personalityOutput[0][3],
        'neuroticism': personalityOutput[0][4],
      },
      'sentiment': _getSentiment(sentimentOutput[0]),
      'relationship_score': relationshipOutput[0][0],
      'inference_time_ms': stopwatch.elapsedMilliseconds,
    };
  }
  
  List<List<int>> _tokenize(String text, {int maxLength = 128}) {
    // Simplified tokenization - integrate with your tokenizer
    // You'll need to port your tokenizer logic or use a Flutter tokenizer package
    final tokens = text.split(' ').take(maxLength).toList();
    final tokenIds = tokens.map((t) => t.hashCode % 30000).toList();
    
    // Pad to maxLength
    while (tokenIds.length < maxLength) {
      tokenIds.add(0);
    }
    
    return [tokenIds.take(maxLength).toList()];
  }
  
  String _getSentiment(List<double> sentimentScores) {
    final maxIndex = sentimentScores.indexOf(
      sentimentScores.reduce((a, b) => a > b ? a : b)
    );
    return ['positive', 'neutral', 'negative'][maxIndex];
  }
  
  void dispose() {
    _interpreter.close();
  }
}

// Usage in your game
class GameController {
  final _ai = UnwrittenAI();
  
  Future<void> initialize() async {
    await _ai.initialize();
  }
  
  Future<void> handleCardInteraction(String interaction) async {
    final analysis = await _ai.analyzeInteraction(interaction);
    
    print('Personality: ${analysis['personality']}');
    print('Sentiment: ${analysis['sentiment']}');
    print('Relationship: ${analysis['relationship_score']}');
    print('Inference time: ${analysis['inference_time_ms']}ms');
    
    // Update game state based on analysis
    updateGameState(analysis);
  }
}
```

### 6.3 Performance Monitoring

```dart
// lib/performance_monitor.dart
import 'package:battery_plus/battery_plus.dart';

class PerformanceMonitor {
  final _battery = Battery();
  List<int> _inferenceTimes = [];
  int _initialBatteryLevel = 100;
  
  Future<void> startSession() async {
    _initialBatteryLevel = await _battery.batteryLevel;
    _inferenceTimes.clear();
  }
  
  void recordInference(int timeMs) {
    _inferenceTimes.add(timeMs);
  }
  
  Future<Map<String, dynamic>> getSessionStats() async {
    final currentLevel = await _battery.batteryLevel;
    final batteryDrain = _initialBatteryLevel - currentLevel;
    
    return {
      'avg_inference_ms': _inferenceTimes.isEmpty 
        ? 0 
        : _inferenceTimes.reduce((a, b) => a + b) / _inferenceTimes.length,
      'max_inference_ms': _inferenceTimes.isEmpty ? 0 : _inferenceTimes.reduce((a, b) => a > b ? a : b),
      'total_inferences': _inferenceTimes.length,
      'battery_drain_percent': batteryDrain,
    };
  }
}
```

---

## Expected Results & Success Metrics

### Model Quality Targets (2025 Standards)

| Metric | Target | Minimum Acceptable |
|--------|--------|-------------------|
| Model Size (INT4) | 2-3MB | <5MB |
| Inference Time (Mid-range phone) | 8-15ms | <20ms |
| Personality Accuracy | >87% | >82% |
| Sentiment Accuracy | >92% | >87% |
| Battery (25 conversations) | <0.8% | <1.5% |
| Memory Usage | <25MB | <40MB |

### Training Timeline Summary

- **Week 1**: Setup + Data (5-7 days with modern tools)
- **Week 2**: Model + LoRA Training (4-6 days)
- **Week 3**: Quantization + Optimization (3-4 days)
- **Week 4**: Integration + Testing (5-7 days)

**Total**: ~20-25 days with LoRA (vs 30+ days traditional)

### Cost Estimates (2025)

- Compute (Google Colab Pro A100): $12-25/month
- Synthetic data (Claude 3.5 Sonnet): $30-40
- Testing (real devices): Use what you have
- **Total**: ~$50-75

---

## Key Improvements Over 2024 Approach

1. **LoRA Training**: 95% fewer trainable parameters, faster training
2. **PyTorch 2.x**: `torch.compile` gives 40%+ speedup automatically
3. **Better Quantization**: INT4/INT2 support, QAT from start
4. **LiteRT**: Improved PyTorch support, better performance
5. **Modern Data**: Claude 3.5 Sonnet for higher quality synthetic data
6. **Multi-Task LoRA**: Better task isolation, less interference

---

## Troubleshooting Guide

### Issue: Model still too large after quantization
```python
# Solution: Use INT4 or even INT2 quantization
from ai_edge_quantizer import quantize
quantize(model_path, output_path, algorithm='int4')

# Or reduce model size further
model = MultiTaskLoRAModel("google/gemma-2-2b", hidden_size=96)
```

### Issue: Slow inference on device
```dart
// Solution: Enable hardware acceleration
InterpreterOptions()
  ..threads = 4
  ..useNnapi = true  // Android
  ..useGpuDelegate = true  // iOS with CoreML
```

### Issue: Accuracy drop after quantization
```python
# Solution: Use QAT (Quantization-Aware Training) from the start
# Train with fake quantization to adapt weights
model = prepare_qat(model)
train(model)  # Model adapts to quantization during training
```

---

## Resources

- [LiteRT Documentation](https://ai.google.dev/edge/litert)
- [AI Edge Torch](https://github.com/google-ai-edge/ai-edge-torch)
- [PEFT Library](https://github.com/huggingface/peft)
- [MTL-LoRA Paper](https://arxiv.org/abs/2410.09437)
- [PyTorch 2.x Compilation](https://pytorch.org/docs/stable/torch.compiler.html)
- [Gemma 3 270M](https://developers.googleblog.com/en/introducing-gemma-3-270m/)

---

**Ready to build your ultra-efficient AI! 🚀**

*This guide reflects 2025 best practices and should provide significantly better results than 2024 approaches.*
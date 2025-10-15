# TFLite Flutter - TensorFlow Lite Integration

**Current Project Version**: ^0.9.0  
**Latest Available Version**: ^0.11.0  
**Recommendation**: ⚠️ UPDATE RECOMMENDED

---

## Overview

TensorFlow Lite Flutter plugin provides a flexible, mobile-friendly API to run TensorFlow Lite models on-device. Perfect for on-device machine learning inference with minimal latency.

## Key Features

- **On-Device Inference**: Run ML models locally (no internet required)
- **Low Latency**: < 15ms inference on modern devices
- **GPU Acceleration**: GPU delegate support for faster inference
- **Multi-Platform**: iOS, Android, and desktop support
- **Quantization**: Support for int8 quantized models
- **Custom Ops**: Register custom operations
- **Multiple Interpreters**: Run multiple models concurrently

## Installation

```yaml
dependencies:
  tflite_flutter: ^0.11.0
```

### Platform-Specific Setup

#### Android (android/app/build.gradle)
```gradle
android {
    aaptOptions {
        noCompress 'tflite'
    }
}
```

#### iOS (ios/Podfile)
```ruby
post_install do |installer|
  installer.pods_project.targets.each do |target|
    flutter_additional_ios_build_settings(target)
    target.build_configurations.each do |config|
      config.build_settings['ENABLE_BITCODE'] = 'NO'
    end
  end
end
```

## Basic Usage

### Load Model

```dart
import 'package:tflite_flutter/tflite_flutter.dart';

class AIService {
  late Interpreter _interpreter;
  
  Future<void> initialize() async {
    try {
      _interpreter = await Interpreter.fromAsset('models/personality_model.tflite');
      print('Model loaded successfully');
      print('Input shape: ${_interpreter.getInputTensor(0).shape}');
      print('Output shape: ${_interpreter.getOutputTensor(0).shape}');
    } catch (e) {
      throw ModelLoadException('Failed to load model: $e');
    }
  }
  
  @override
  void dispose() {
    _interpreter.close();
  }
}
```

### Run Inference

```dart
Future<List<double>> predict(List<double> input) async {
  // Prepare input tensor
  final inputTensor = [input]; // Shape: [1, inputSize]
  
  // Prepare output tensor
  final outputTensor = List.generate(
    1,
    (_) => List<double>.filled(5, 0), // Shape: [1, 5] for Big Five traits
  );
  
  // Run inference
  final stopwatch = Stopwatch()..start();
  _interpreter.run(inputTensor, outputTensor);
  stopwatch.stop();
  
  AppLogger.ai('Inference completed', metrics: {
    'duration_ms': stopwatch.elapsedMilliseconds,
  });
  
  return outputTensor[0];
}
```

### GPU Acceleration

```dart
Future<void> initializeWithGPU() async {
  try {
    // Try GPU delegate first
    final options = InterpreterOptions()
      ..addDelegate(GpuDelegateV2());
    
    _interpreter = await Interpreter.fromAsset(
      'models/personality_model.tflite',
      options: options,
    );
    
    print('GPU delegate loaded successfully');
  } catch (e) {
    // Fallback to CPU
    print('GPU delegate not available, using CPU');
    _interpreter = await Interpreter.fromAsset('models/personality_model.tflite');
  }
}
```

## Advanced Features

### Multiple Inputs/Outputs

```dart
// Multiple inputs
final inputs = {
  0: textFeatures,  // First input tensor
  1: audioFeatures, // Second input tensor
};

// Multiple outputs
final outputs = {
  0: List.filled(5, 0.0),     // Personality traits
  1: List.filled(3, 0.0),     // Sentiment scores
};

_interpreter.runForMultipleInputs(inputs, outputs);
```

### Quantized Models (int8)

```dart
// Input: List<int> (0-255)
final quantizedInput = input.map((v) => (v * 255).toInt()).toList();

// Output: List<int>
final quantizedOutput = List<int>.filled(outputSize, 0);

_interpreter.run([quantizedInput], [quantizedOutput]);

// Dequantize output
final output = quantizedOutput.map((v) => v / 255.0).toList();
```

### Dynamic Input Shapes

```dart
// Resize input tensor
_interpreter.resizeInputTensor(0, [1, 256]); // New shape
_interpreter.allocateTensors(); // Reallocate memory

// Run inference with new shape
_interpreter.run(newInput, output);
```

### Model Metadata

```dart
final inputTensor = _interpreter.getInputTensor(0);
print('Input shape: ${inputTensor.shape}');
print('Input type: ${inputTensor.type}');
print('Input name: ${inputTensor.name}');

final outputTensor = _interpreter.getOutputTensor(0);
print('Output shape: ${outputTensor.shape}');
print('Output type: ${outputTensor.type}');
```

## Unwritten Integration

### Personality Model Service

```dart
class PersonalityInferenceService {
  late Interpreter _interpreter;
  bool _isInitialized = false;
  
  static const int inputSize = 128;
  static const int outputSize = 5; // Big Five traits
  
  Future<void> initialize() async {
    if (_isInitialized) return;
    
    try {
      // Load model with GPU support
      final options = InterpreterOptions();
      
      if (Platform.isAndroid || Platform.isIOS) {
        try {
          options.addDelegate(GpuDelegateV2());
        } catch (e) {
          print('GPU not available, using CPU');
        }
      }
      
      _interpreter = await Interpreter.fromAsset(
        'assets/models/personality_model.tflite',
        options: options,
      );
      
      _isInitialized = true;
      AppLogger.info('Personality model loaded');
    } catch (e) {
      throw ModelLoadException('Failed to load personality model: $e');
    }
  }
  
  Future<Map<String, double>> predictPersonality(String text) async {
    if (!_isInitialized) await initialize();
    
    // Preprocess text to features
    final features = _preprocessText(text);
    
    // Run inference
    final input = [features];
    final output = List.generate(1, (_) => List<double>.filled(outputSize, 0));
    
    final stopwatch = Stopwatch()..start();
    _interpreter.run(input, output);
    stopwatch.stop();
    
    // Check performance target (< 15ms)
    if (stopwatch.elapsedMilliseconds > 15) {
      AppLogger.performance('Slow inference', stopwatch.elapsed);
    }
    
    // Map output to Big Five traits
    final traits = output[0];
    return {
      'openness': traits[0],
      'conscientiousness': traits[1],
      'extraversion': traits[2],
      'agreeableness': traits[3],
      'neuroticism': traits[4],
    };
  }
  
  List<double> _preprocessText(String text) {
    // TODO: Implement text preprocessing
    // - Tokenization
    // - Embedding lookup
    // - Normalization
    return List.filled(inputSize, 0.0);
  }
  
  void dispose() {
    if (_isInitialized) {
      _interpreter.close();
      _isInitialized = false;
    }
  }
}
```

## Best Practices

1. **Initialize Once**: Load model once at app startup
2. **Check Performance**: Target < 15ms inference
3. **Battery Optimization**: Reduce inference frequency on low battery
4. **Fallback Logic**: Have rule-based fallback if model fails
5. **Model Size**: Keep models < 5MB for fast loading
6. **Quantization**: Use int8 quantization for smaller size
7. **Caching**: Cache recent predictions
8. **Threading**: Run inference on background thread (use `compute()`)

## Performance Targets (Unwritten)

- ✅ **< 15ms** inference time
- ✅ **< 10%** battery drain per 30min session
- ✅ **< 5MB** model size
- ✅ **60 FPS** maintained during inference

## Resources

- **Official Documentation**: https://pub.dev/packages/tflite_flutter
- **GitHub Repository**: https://github.com/am15h/tflite_flutter_plugin
- **TensorFlow Lite Guide**: https://www.tensorflow.org/lite/guide
- **Model Optimization**: https://www.tensorflow.org/lite/performance/model_optimization

## Model Conversion

Convert TensorFlow models to TFLite:

```bash
# Python
import tensorflow as tf

# Load SavedModel
converter = tf.lite.TFLiteConverter.from_saved_model('model/')

# Optimize for size and speed
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.int8]

# Convert
tflite_model = converter.convert()

# Save
with open('model.tflite', 'wb') as f:
  f.write(tflite_model)
```

---

**Last Updated**: October 14, 2025  
**Update Priority**: High (performance improvements in 0.11.0)


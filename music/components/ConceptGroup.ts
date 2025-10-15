/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/
import { css, html, LitElement } from 'lit';
import { customElement, property } from 'lit/decorators.js';
import './ParameterSlider';

type GroupType = 'independent' | 'sum-to-100';

@customElement('concept-group')
export class ConceptGroup extends LitElement {
  static override styles = css`
    :host {
      display: block;
      padding: 2vmin;
      background: rgba(0, 0, 0, 0.2);
      border-radius: 1vmin;
      border: 1px solid rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
    }
    .title {
      font-weight: 500;
      font-size: 2vmin;
      margin-bottom: 1.5vmin;
      color: #fff;
      text-align: center;
      min-height: 4.5vmin;
    }
    .sliders {
      display: flex;
      flex-direction: column;
      gap: 1.5vmin;
    }
  `;

  @property({ type: String }) title = '';
  @property({ type: String }) type: GroupType = 'independent';
  @property({ type: Array }) labels: string[] = [];
  @property({ type: Array }) values: number[] = [50, 50, 50];

  private handleSliderInput(index: number, e: CustomEvent<number>) {
    const newValue = e.detail;
    let newValues = [...this.values];
    newValues[index] = newValue;

    if (this.type === 'sum-to-100') {
      const remainder = 100 - newValue;
      const otherIndices = [0, 1, 2].filter(i => i !== index);
      const [i0, i1] = otherIndices;

      const oldSumOfOthers = this.values[i0] + this.values[i1];

      // If other sliders had a value, maintain their ratio. Otherwise, split the remainder.
      if (oldSumOfOthers > 1e-9) {
        const ratio = this.values[i0] / oldSumOfOthers;
        const val0 = remainder * ratio;
        newValues[i0] = val0;
        newValues[i1] = remainder - val0; // This is more precise than multiplying by (1 - ratio)
      } else {
        newValues[i0] = remainder / 2;
        newValues[i1] = remainder / 2;
      }
    }
    
    // Final sanity check to prevent any possible NaN from propagating.
    if (newValues.some(v => isNaN(v))) {
      console.error('NaN detected in values, resetting group.', this.title);
      newValues = [100/3, 100/3, 100/3];
    }

    this.values = newValues;
    this.dispatchEvent(new CustomEvent('values-changed', { detail: this.values, bubbles: true, composed: true }));
  }

  override render() {
    return html`
      <div class="title">${this.title}</div>
      <div class="sliders">
        ${this.labels.map((label, i) => html`
          <parameter-slider
            .label=${label}
            .value=${this.values[i]}
            @input=${(e: CustomEvent<number>) => this.handleSliderInput(i, e)}
          ></parameter-slider>
        `)}
      </div>
    `;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    'concept-group': ConceptGroup;
  }
}
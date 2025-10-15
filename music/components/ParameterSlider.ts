/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/
import { css, html, LitElement } from 'lit';
import { customElement, property } from 'lit/decorators.js';

@customElement('parameter-slider')
export class ParameterSlider extends LitElement {
  static override styles = css`
    :host {
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 100%;
      font-size: 1.6vmin;
    }
    .label {
      font-weight: 400;
      color: #ddd;
      margin-bottom: 0.8vmin;
    }
    .slider-container {
      display: flex;
      align-items: center;
      width: 100%;
    }
    input[type='range'] {
      flex-grow: 1;
      margin: 0 1vmin;
      cursor: ew-resize;
    }
    .value {
      width: 4ch;
      text-align: right;
      font-family: monospace;
      font-size: 1.8vmin;
      color: #fff;
    }
  `;

  @property({ type: String }) label = '';
  @property({ type: Number }) value = 50;
  @property({ type: Number }) min = 0;
  @property({ type: Number }) max = 100;

  private onInput(e: Event) {
    const target = e.target as HTMLInputElement;
    this.value = Number(target.value);
    this.dispatchEvent(new CustomEvent('input', { detail: this.value, bubbles: true, composed: true }));
  }

  override render() {
    return html`
      <div class="label">${this.label}</div>
      <div class="slider-container">
        <input
          type="range"
          .min=${this.min}
          .max=${this.max}
          .value=${this.value}
          @input=${this.onInput}
        />
        <div class="value">${Math.round(this.value)}</div>
      </div>
    `;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    'parameter-slider': ParameterSlider;
  }
}

class SeventeenTrackCard extends HTMLElement {
  setConfig(config) {
    if (!config.entity) {
      throw new Error('You need to define an entity');
    }
    this.config = config;
  }

  getCardSize() {
    return 3;
  }

  set hass(hass) {
    const entityId = this.config.entity;
    const state = hass.states[entityId];
    const packages = state.attributes.packages != null ? state.attributes.packages : [];

    if (!this.content) {
      const card = document.createElement('ha-card');
      const style = document.createElement('style');
      this.content = document.createElement('div');

      card.header = this.config.title != null ? this.config.title : '17Track.net';
      style.textContent = `
        table {
          width: 100%;
          padding: 0 32px 32px 32px;
        }
        thead th {
          text-align: left;
        }
        tbody tr:nth-child(odd) {
          background-color: var(--paper-card-background-color);
        }
        tbody tr:nth-child(even) {
          background-color: var(--secondary-background-color);
        }
        td a {
          color: var(--primary-text-color);
          font-weight: normal;
        }
      `;

      card.appendChild(this.content);
      this.appendChild(style);
      this.appendChild(card);
    }

    let card_content = `
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Status</th>
          </tr>
        </thead>
      <tbody>
    `;

    const updated_content = `
      ${packages.map(elem => `
          <tr>
            <td>
              <a href="https://17track.net/en/track#nums=${elem.tracking_number}" target='_blank'>
                ${elem.friendly_name != null ? elem.friendly_name : elem.tracking_number}
              </a>
            </td>
            <td>${elem.info_text}</td>
          </tr>
      `).join('')}
    `;
    card_content += updated_content;
    card_content += `</tbody></table>`;

    this.content.innerHTML = card_content;
  }
}

customElements.define('seventeen-track-card', SeventeenTrackCard);

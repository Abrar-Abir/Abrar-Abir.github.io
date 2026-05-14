---
layout: page
title: chess
permalink: /chess/
description: rapid stats from chess.com, refreshed daily
nav: true
nav_order: 4
chart:
  chartjs: true
---

<style>
  .chess-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.25rem;
    margin-bottom: 1.5rem;
  }
  @media (min-width: 600px) {
    .chess-grid { grid-template-columns: 1fr 1fr; }
  }
  .chess-card {
    border: 1px solid var(--global-divider-color);
    border-radius: 6px;
    padding: 1rem 1.25rem;
  }
  .chess-card h3 { margin-top: 0; margin-bottom: 0.5rem; }
  .chess-profile { display: flex; align-items: center; gap: 1rem; }
  .chess-profile img {
    width: 64px; height: 64px; border-radius: 50%; object-fit: cover;
  }
  .chess-profile .meta { font-size: 0.9rem; color: var(--global-text-color-light); }
  .chess-stat-row {
    display: flex; justify-content: space-between; margin: 0.25rem 0;
    font-variant-numeric: tabular-nums;
  }
  .chess-bar {
    display: flex; height: 10px; border-radius: 5px; overflow: hidden;
    background: var(--global-divider-color); margin: 0.5rem 0;
  }
  .chess-bar .w { background: #4caf50; }
  .chess-bar .l { background: #e53935; }
  .chess-bar .d { background: #9e9e9e; }
  .chess-empty { color: var(--global-text-color-light); font-style: italic; }
  #chess-chart-wrap { position: relative; height: 320px; }
</style>

<div id="chess-content">
  <p class="chess-empty">loading…</p>
</div>

<script>
  (function () {
    const dataUrl = "{{ '/assets/data/chess_stats.json' | relative_url }}";
    const root = document.getElementById("chess-content");

    function flagEmoji(cc) {
      if (!cc || cc.length !== 2) return "";
      const base = 0x1f1e6 - "A".charCodeAt(0);
      return String.fromCodePoint(base + cc.charCodeAt(0), base + cc.charCodeAt(1));
    }

    function timeAgo(iso) {
      if (!iso) return "never";
      const diff = (Date.now() - new Date(iso).getTime()) / 1000;
      if (diff < 3600) return Math.round(diff / 60) + " min ago";
      if (diff < 86400) return Math.round(diff / 3600) + " h ago";
      return Math.round(diff / 86400) + " d ago";
    }

    function pct(n, d) { return d ? Math.round((n / d) * 1000) / 10 : 0; }

    function render(data) {
      const p = data.profile || {};
      const r = (data.stats || {}).chess_rapid || null;
      const history = ((data.rating_history || {}).rapid) || [];

      const hasData = data.fetched_at && (p.username || r);
      if (!hasData) {
        root.innerHTML = '<p class="chess-empty">no data yet — the daily fetch job hasn\'t run.</p>';
        return;
      }

      const flag = flagEmoji(p.country_code);
      const joinedYear = p.joined ? new Date(p.joined * 1000).getFullYear() : null;
      const titleBadge = p.title ? '<strong style="color:#b71c1c;">' + p.title + '</strong> ' : '';

      let cardHtml = "";
      if (r && r.last) {
        const w = (r.record && r.record.win) || 0;
        const l = (r.record && r.record.loss) || 0;
        const d = (r.record && r.record.draw) || 0;
        const total = w + l + d;
        const winRate = pct(w, total);
        const best = (r.best && r.best.rating) || "—";
        cardHtml = '' +
          '<div class="chess-card">' +
          '<h3>rapid</h3>' +
          '<div class="chess-stat-row"><span>current</span><strong>' + (r.last.rating || "—") + '</strong></div>' +
          '<div class="chess-stat-row"><span>best</span><strong>' + best + '</strong></div>' +
          '<div class="chess-bar" title="W ' + w + ' / L ' + l + ' / D ' + d + '">' +
            (total ? '<div class="w" style="width:' + pct(w, total) + '%"></div>' : '') +
            (total ? '<div class="l" style="width:' + pct(l, total) + '%"></div>' : '') +
            (total ? '<div class="d" style="width:' + pct(d, total) + '%"></div>' : '') +
          '</div>' +
          '<div class="chess-stat-row"><span>W / L / D</span><span>' + w + ' / ' + l + ' / ' + d + '</span></div>' +
          '<div class="chess-stat-row"><span>win rate</span><span>' + winRate + '%</span></div>' +
          '</div>';
      } else {
        cardHtml = '<div class="chess-card"><h3>rapid</h3><p class="chess-empty">no rapid stats.</p></div>';
      }

      root.innerHTML =
        '<div class="chess-grid">' +
          '<div class="chess-card chess-profile">' +
            (p.avatar ? '<img src="' + p.avatar + '" alt="">' : '') +
            '<div>' +
              '<h3 style="margin:0;">' + titleBadge +
                (p.url ? '<a href="' + p.url + '" target="_blank" rel="noopener">' + (p.username || "") + '</a>' : (p.username || "")) +
                ' ' + flag +
              '</h3>' +
              '<div class="meta">' +
                (joinedYear ? "joined " + joinedYear : "") +
                (p.followers != null ? " · " + p.followers + " followers" : "") +
                ' · updated ' + timeAgo(data.fetched_at) +
              '</div>' +
            '</div>' +
          '</div>' +
          cardHtml +
        '</div>' +
        '<div class="chess-card"><h3>rapid rating — last ' + history.length + ' months</h3>' +
          (history.length ? '<div id="chess-chart-wrap"><canvas id="chess-chart"></canvas></div>'
                          : '<p class="chess-empty">no rating history yet.</p>') +
        '</div>';

      if (history.length) drawChart(history);
    }

    let chartInstance = null;
    function themeColor() {
      const s = getComputedStyle(document.documentElement);
      return s.getPropertyValue("--global-theme-color").trim() || "#b71c1c";
    }
    function textColor() {
      const s = getComputedStyle(document.documentElement);
      return s.getPropertyValue("--global-text-color").trim() || "#000";
    }

    function drawChart(history) {
      if (typeof Chart === "undefined") {
        // chartjs.liquid loads with defer; retry once it's ready.
        setTimeout(function () { drawChart(history); }, 100);
        return;
      }
      const ctx = document.getElementById("chess-chart").getContext("2d");
      const color = themeColor();
      const tc = textColor();
      if (chartInstance) chartInstance.destroy();
      chartInstance = new Chart(ctx, {
        type: "line",
        data: {
          labels: history.map(function (h) { return h.month; }),
          datasets: [{
            label: "rapid rating",
            data: history.map(function (h) { return h.rating; }),
            borderColor: color,
            backgroundColor: color + "33",
            tension: 0.25,
            pointRadius: 3,
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { labels: { color: tc } } },
          scales: {
            x: { ticks: { color: tc }, grid: { color: tc + "22" } },
            y: { ticks: { color: tc }, grid: { color: tc + "22" } },
          },
        },
      });
    }

    // Re-color chart when user toggles light/dark theme.
    new MutationObserver(function () {
      if (chartInstance) {
        const c = themeColor();
        const tc = textColor();
        chartInstance.data.datasets[0].borderColor = c;
        chartInstance.data.datasets[0].backgroundColor = c + "33";
        chartInstance.options.plugins.legend.labels.color = tc;
        chartInstance.options.scales.x.ticks.color = tc;
        chartInstance.options.scales.y.ticks.color = tc;
        chartInstance.options.scales.x.grid.color = tc + "22";
        chartInstance.options.scales.y.grid.color = tc + "22";
        chartInstance.update();
      }
    }).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });

    fetch(dataUrl)
      .then(function (r) { return r.json(); })
      .then(render)
      .catch(function () {
        root.innerHTML = '<p class="chess-empty">failed to load chess stats.</p>';
      });
  })();
</script>

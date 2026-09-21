/* Tiny dependency-free bar chart renderer (canvas-based), so the dashboard
   works fully offline without pulling in a charting library from a CDN. */
function renderBarChart(canvasId, labels, values) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const width = canvas.width = canvas.clientWidth * 2;
  const height = canvas.height = canvas.clientHeight * 2;
  ctx.scale(1, 1);

  const padding = 40 * 2;
  const chartWidth = width - padding * 1.2;
  const chartHeight = height - padding;
  const max = Math.max(...values, 1);
  const barGap = 16 * 2;
  const barWidth = (chartWidth - barGap * (values.length - 1)) / values.length;

  ctx.clearRect(0, 0, width, height);
  ctx.font = `${16 * 2}px -apple-system, Roboto, sans-serif`;
  ctx.fillStyle = '#6b6b6b';
  ctx.textAlign = 'center';

  values.forEach((value, i) => {
    const barHeight = (value / max) * (chartHeight - 20);
    const x = padding * 0.6 + i * (barWidth + barGap);
    const y = height - padding / 1.5 - barHeight;

    ctx.fillStyle = '#c97b3f';
    ctx.beginPath();
    ctx.roundRect(x, y, barWidth, barHeight, [6, 6, 0, 0]);
    ctx.fill();

    ctx.fillStyle = '#3e2820';
    ctx.fillText(value.toLocaleString(undefined, {maximumFractionDigits: 0}), x + barWidth / 2, y - 8);

    ctx.fillStyle = '#6b6b6b';
    ctx.fillText(labels[i], x + barWidth / 2, height - padding / 1.5 + 24);
  });
}

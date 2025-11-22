(function ($, window, document) {
  const canvasSelector = '#lcdBurstCanvas';
  const BURST_DURATION = 650;

  function getCanvas() {
    return $(canvasSelector);
  }

  function createLine($canvas, config) {
    const { startX, startY, deltaX, deltaY, angle, width } = config;
    const $line = $('<span/>', { class: 'burst-line' }).appendTo($canvas);
    $line.css({
      left: startX,
      top: startY,
      width: width || 120,
      transform: `rotate(${angle}deg)`,
      opacity: 0.98,
    });

    $line.animate(
      {
        left: startX + deltaX,
        top: startY + deltaY,
        opacity: 0,
      },
      BURST_DURATION,
      'swing',
      () => $line.remove(),
    );
  }

  function buildConfigs(rect, isOn) {
    const direction = isOn ? 1 : -1;
    const centerY = rect.top + rect.height / 2;
    const edgeX = direction === 1 ? rect.right - 8 : rect.left + 8;

    return [
      {
        // middle beam from thumb edge
        startX: edgeX,
        startY: centerY,
        deltaX: direction * 250,
        deltaY: 0,
        angle: direction === 1 ? 0 : 180,
        width: 140,
      },
      {
        // top flare
        startX: edgeX,
        startY: rect.top + rect.height * 0.2,
        deltaX: direction * 220,
        deltaY: -110,
        angle: direction === 1 ? -22 : 202,
        width: 110,
      },
      {
        // bottom flare
        startX: edgeX,
        startY: rect.bottom - rect.height * 0.2,
        deltaX: direction * 220,
        deltaY: 110,
        angle: direction === 1 ? 22 : 158,
        width: 110,
      },
    ];
  }

  function triggerBurst(isOn, trackEl) {
    if (!trackEl) return;
    const rect = trackEl.getBoundingClientRect();
    const $canvas = getCanvas();
    if (!$canvas.length) return;

    const configs = buildConfigs(rect, isOn);
    configs.forEach((config, idx) => {
      setTimeout(() => createLine($canvas, config), idx * 40);
    });
  }

  window.LcdBurstAnimator = { trigger: triggerBurst };
})(jQuery, window, document);

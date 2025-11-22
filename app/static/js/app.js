(function ($) {
  const config = window.APP_CONFIG || {};
  const models = Array.isArray(config.models) ? config.models : [];
  const refreshInterval = Number(config.refreshInterval) || 60000;
  const initialLcdFlag = typeof config.lcdModeEnabled === 'boolean' ? config.lcdModeEnabled : true;
  let lcdModeEnabled = initialLcdFlag;
  let refreshTimerId = null;

  function getCookie(name) {
    const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
    return match ? decodeURIComponent(match[1]) : null;
  }

  function setCookie(name, value, days) {
    const maxAge = days ? days * 24 * 60 * 60 : undefined;
    let cookie = `${name}=${encodeURIComponent(value)}; path=/; SameSite=Lax`;
    if (maxAge) {
      cookie += `; max-age=${maxAge}`;
    }
    document.cookie = cookie;
  }

  function setLoadingState($iframe, isLoading) {
    const $skeleton = $iframe.siblings('.clock-skeleton');
    if (isLoading) {
      $skeleton.addClass('is-visible');
      $iframe.removeClass('is-ready');
    } else {
      $skeleton.removeClass('is-visible');
      $iframe.addClass('is-ready');
    }
  }

  function buildClockCard(model) {
    const $card = $('<section/>', {
      class: 'clock-card',
      'data-model-card': model.id,
    });

    const $frameWrapper = $('<div/>', { class: 'clock-frame-wrapper' });
    const $iframe = $('<iframe/>', {
      class: 'clock-frame',
      title: `${model.label} digital clock`,
      'data-model': model.id,
      loading: 'lazy',
    });
    const $skeleton = $('<div/>', {
      class: 'clock-skeleton is-visible',
      'aria-hidden': 'true',
    });

    $iframe.on('load', function handleLoad() {
      if (this.src === 'about:blank') return;
      setLoadingState($(this), false);
    });

    $frameWrapper.append($iframe, $skeleton);

    const $meta = $('<div/>', { class: 'clock-meta' });
    const $logo = $('<img/>', {
      class: 'clock-logo',
      src: model.logo,
      alt: `${model.label} logo`,
      width: 44,
      height: 44,
    });

    const $text = $('<div/>', { class: 'clock-text' });
    $text.append($('<span/>', { class: 'clock-model', text: model.label }));
    $text.append($('<span/>', { class: 'clock-provider', text: model.provider }));

    $meta.append($logo, $text);
    $card.append($frameWrapper, $meta);

    return $card;
  }

  function getClientTimeStamp() {
    const now = new Date();
    const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC';
    const time = now.toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false,
    });
    return `current time is ${time} ${tz}`;
  }

  function refreshFrames() {
    const clientTime = getClientTimeStamp();
    $('.clock-frame').each(function refresh() {
      const modelId = $(this).data('model');
      const $frame = $(this);
      setLoadingState($frame, true);
      this.src = 'about:blank';

      const params = new URLSearchParams({
        model: modelId,
        current_time: clientTime,
        ts: Date.now().toString(),
      });
      const targetSrc = `/clock/render?${params.toString()}`;

      setTimeout(() => {
        this.src = targetSrc;
      }, 75);
    });
  }

  function restartRefreshTimer() {
    if (refreshTimerId) {
      clearInterval(refreshTimerId);
    }
    refreshTimerId = setInterval(refreshFrames, refreshInterval);
  }

  function syncLcdModeFromCookie() {
    const cookieValue = getCookie('lcd_mode');
    if (cookieValue === null) {
      lcdModeEnabled = true;
      setCookie('lcd_mode', '1', 365);
      return;
    }
    lcdModeEnabled = cookieValue === '1';
  }

  function setLcdMode(enabled, options = {}) {
    const { animate = false } = options;
    if (lcdModeEnabled === enabled) return;
    lcdModeEnabled = enabled;
    setCookie('lcd_mode', enabled ? '1' : '0', 365);
    updateToggleUI();
    if (animate) triggerToggleBurst();
    refreshFrames();
    restartRefreshTimer();
  }

  function updateToggleUI() {
    const $toggle = $('#lcdToggle');
    if (!$toggle.length) return;
    $toggle.attr('aria-pressed', String(lcdModeEnabled));
    $toggle.toggleClass('is-active', lcdModeEnabled);
  }

  function triggerToggleBurst() {
    const animator = window.LcdBurstAnimator;
    if (!animator || typeof animator.trigger !== 'function') return;
    const trackEl = document.querySelector('#lcdToggle .lcd-toggle-track');
    if (!trackEl) return;
    animator.trigger(lcdModeEnabled, trackEl);
  }

  $(function init() {
    const $grid = $('#clocks-grid');
    if (!$grid.length) return;

    syncLcdModeFromCookie();

    models.forEach((model) => {
      const $card = buildClockCard(model);
      $grid.append($card);
    });

    updateToggleUI();

    $('#lcdToggle').on('click', () => {
      const nextState = !lcdModeEnabled;
      setLcdMode(nextState, { animate: true });
    });

    refreshFrames();
    restartRefreshTimer();
  });
})(jQuery);

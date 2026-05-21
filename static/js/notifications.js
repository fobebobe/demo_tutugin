(function() {
    'use strict';

    window.showNotification = function(message, type) {
        var container = document.getElementById('notification-container');
        var notification = document.createElement('div');
        notification.className = 'custom-notification notification-' + type;

        var icon = '';
        if (type === 'success') icon = '✓';
        else if (type === 'error') icon = '✕';
        else if (type === 'warning') icon = '⚠';
        else icon = 'ℹ';

        notification.innerHTML = '<span class="notif-icon">' + icon + '</span>' +
            '<span class="notif-text">' + message + '</span>' +
            '<button class="notif-close" onclick="this.parentElement.remove()">×</button>';

        container.appendChild(notification);

      
        setTimeout(function() {
            notification.classList.add('notif-show');
        }, 10);

        // таймер на автоудаление через 4 секунды
        setTimeout(function() {
            notification.classList.remove('notif-show');
            notification.classList.add('notif-hide');
            setTimeout(function() {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 400);
        }, 4000);
    };
})();

'use strict';

document.querySelectorAll('.book-item').forEach(item => {
            item.addEventListener('click', () => {
                const title = item.getAttribute('data-title');
                navigator.clipboard.writeText(title)
                    .then(() => {
                        alert(`Copied to clipboard: ${title}`);
                    })
                    .catch(err => {
                        console.error('Failed to copy: ', err);
                    });
            });
        });
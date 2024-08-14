// main.js
document.getElementById('like-icon').addEventListener('click', function () {
    fetch('/like', {
        method: 'POST'
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('like-count').innerText = data.like_count;
        })
        .catch(error => console.error('Error:', error));
});
    // 页面加载时获取当前的爱心计数
    window.onload = function() {
    fetch('/get_like_count')
        .then(response => response.json())
        .then(data => {
            document.getElementById('like-count').innerText = data.like_count;
        })
        .catch(error => console.error('Error:', error));
};

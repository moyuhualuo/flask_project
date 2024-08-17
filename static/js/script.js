// 为每个 .like-icon 元素添加点击事件监听器
document.querySelectorAll('.like-icon').forEach(icon => {
    icon.addEventListener('click', function () {
        const itemId = this.getAttribute('data-item-id');
        fetch(`/like/${itemId}`, {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                // 更新对应 item_id 的计数器
                document.querySelector(`.like-count[data-item-id="${itemId}"]`).innerText = data.like_count;
            })
            .catch(error => console.error('Error:', error));
    });
});

// 页面加载时获取每个 .like-count 的初始计数
window.onload = function () {
    document.querySelectorAll('.like-count').forEach(count => {
        const itemId = count.getAttribute('data-item-id');
        fetch(`/get_like_count/${itemId}`)
            .then(response => response.json())
            .then(data => {
                count.innerText = data.like_count;
            })
            .catch(error => console.error('Error:', error));
    });
};

function showEditForm(contentId) {
    // 隐藏其他所有表单
    var forms = document.querySelectorAll('[id^="edit-form-"]');
    forms.forEach(function (form) {
        form.style.display = 'none';
    });

    // 只显示当前的编辑表单
    document.getElementById('edit-form-' + contentId).style.display = 'block';
}

function hideEditForm(contentId) {
    document.getElementById('edit-form-' + contentId).style.display = 'none';
}



function showAddForm() {
    // Hide edit forms if shown
    const editForms = document.querySelectorAll('[id^="edit-form-"]');
    editForms.forEach(form => form.style.display = 'none');

    const form = document.getElementById('add-form');
    form.style.display = 'block';
}

    function hideAddForm() {
    document.getElementById('add-form').style.display = 'none';
}


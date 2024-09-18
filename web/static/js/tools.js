document.getElementById('addButton').addEventListener('click', function () {
    var inputForm = document.getElementById('inputForm');
    inputForm.style.display = 'block'; // 显示输入表单
});
document.getElementById('cancelButton').addEventListener('click', function () {
    document.getElementById('inputForm').style.display = 'none';
});

function showEditForm(webId) {
    document.getElementById('edit-form-' + webId).style.display = 'block';
}

function hideEditForm(webId) {
    document.getElementById('edit-form-' + webId).style.display = 'none';
}
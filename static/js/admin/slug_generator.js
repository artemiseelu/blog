(function($) {
    $(document).ready(function() {
        // 获取标题和 slug 输入框
        var titleInput = $('#id_title');
        var slugInput = $('#id_slug');
        
        // 监听标题输入
        titleInput.on('keyup change', function() {
            if (!slugInput.data('manual')) {  // 如果 slug 未被手动修改
                var title = $(this).val();
                // 发送 AJAX 请求生成 slug
                $.get('/admin/generate-slug/', {title: title}, function(data) {
                    slugInput.val(data.slug);
                });
            }
        });
        
        // 监听 slug 手动修改
        slugInput.on('keyup change', function() {
            $(this).data('manual', true);
        });
    });
})(django.jQuery); 
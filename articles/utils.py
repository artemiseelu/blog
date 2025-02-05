import uuid
import re
from pypinyin import pinyin, Style
from django.utils.text import slugify

def generate_slug(title):
    """生成文章的 slug
    
    如果是中文标题，转换为拼音
    如果是中英混合，保留英文部分，中文转拼音
    如果转换失败，使用 uuid
    使用下划线作为分隔符
    """
    try:
        # 分离中英文
        words = []
        current_word = ''
        
        for char in title:
            if '\u4e00' <= char <= '\u9fff':  # 是中文字符
                if current_word:  # 如果有累积的非中文字符
                    words.append(current_word)
                    current_word = ''
                # 转换中文字符为拼音
                py = pinyin(char, style=Style.NORMAL)[0][0]
                words.append(py)
            else:
                current_word += char
        
        # 添加最后累积的非中文字符
        if current_word:
            words.append(current_word)
        
        # 合并所有部分并生成slug
        combined = ' '.join(words)
        # 先用 slugify 处理，然后将连字符替换为下划线
        slug = slugify(combined).replace('-', '_')
        
        # 如果生成的slug太短或为空，添加随机字符
        if len(slug) < 3:
            slug = f"{slug}_r{str(uuid.uuid4())[:6]}"
        
        return slug
    except Exception as e:
        print(f"Slug generation error: {e}")  # 添加错误日志
        # 发生错误时使用uuid，同样使用下划线
        return f"article_{str(uuid.uuid4())[:8]}" 
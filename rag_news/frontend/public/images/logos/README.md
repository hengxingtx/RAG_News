# 如何添加自定义Logo

请按照以下步骤添加您的自定义Logo：

1. 准备您的Logo图片文件，建议尺寸约为 200x80 像素，格式为PNG或SVG（推荐使用透明背景）

2. 将您的图片文件命名为 `my-logo.png`（或者您喜欢的其他名称）

3. 将图片文件复制到此目录 (`rag_news/frontend/public/images/logos/`)

4. 如果您使用了不同的文件名，请修改 `src/pages/Login.tsx` 文件中的图片路径：

```jsx
<img 
    src="/images/logos/您的文件名.扩展名" 
    alt="Logo" 
    className="login-logo-image"
/>
```

5. 如果需要调整Logo大小，可以修改 `src/pages/Login.css` 文件中的 `.login-logo-image` 样式：

```css
.login-logo-image {
    height: 80px; /* 调整此值以更改Logo高度 */
    margin-bottom: 15px;
    display: block;
    margin-left: auto;
    margin-right: auto;
}
```

6. 刷新页面，查看效果 
# RAG NEWS 艺术字体样式指南

我们提供了几种不同风格的艺术字体供您选择。您可以通过修改 `Login.tsx` 文件中的类名来切换不同风格。

## 如何更换字体风格

在 `Login.tsx` 文件中找到如下代码：

```jsx
<h1 className="art-title">RAG NEWS</h1>
```

只需要更改 `className` 的值，就可以切换到不同的风格。

## 可用的字体风格

1. **默认科技风** (默认选择)
   ```jsx
   <h1 className="art-title">RAG NEWS</h1>
   ```
   特点：霓虹蓝色科技感渐变，带发光效果

2. **游戏风格**
   ```jsx
   <h1 className="art-title-game">RAG NEWS</h1>
   ```
   特点：像素风格，8位游戏机复古效果

3. **金属风格**
   ```jsx
   <h1 className="art-title-metal">RAG NEWS</h1>
   ```
   特点：金属质感渐变，带阴影

4. **未来风格**
   ```jsx
   <h1 className="art-title-future">RAG NEWS</h1>
   ```
   特点：强烈霓虹效果，科幻感十足

5. **凸起质感**
   ```jsx
   <h1 className="art-title-emboss">RAG NEWS</h1>
   ```
   特点：3D浮雕效果，突出文字

## 调整字体大小

如果您想调整字体大小，请在 `Login.css` 文件中找到相应的样式类，并修改 `font-size` 属性的值：

```css
/* 例如，调整游戏风格的字体大小 */
.art-title-game {
    font-size: 40px; /* 修改这个值来调整字体大小 */
    /* 其他样式 */
}
```

各种风格的字体大小值：
- 默认科技风：`art-title` 默认是 46px
- 游戏风格：`art-title-game` 默认是 40px
- 金属风格：`art-title-metal` 默认是 46px
- 未来风格：`art-title-future` 默认是 42px
- 凸起质感：`art-title-emboss` 默认是 40px

小屏幕下的字体大小也可以在 `@media (max-width: 992px)` 部分进行调整。

## 自定义

如果您想进一步自定义，可以在 `Login.css` 文件中修改相应的样式类。

每种字体风格都有：
- 特定的字体家族
- 特定的颜色和文字效果
- 响应式设计，适应不同屏幕大小 
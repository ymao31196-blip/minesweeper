$env:DEEPSEEK_API_KEY = [Environment]::GetEnvironmentVariable("DEEPSEEK_API_KEY", "User")

Set-Location "C:\Users\86183\Desktop\游戏项目"

$cacheBuster = "[run@" + (Get-Date -Format "HHmmss") + "]"

$task = "任务：开发一个网页版扫雷游戏（Minesweeper），单文件 HTML/JS/CSS，可直接在浏览器打开。默认9×9网格10个地雷，支持初中高级三档难度选择。左键翻开、右键标记旗帜、0格自动展开、首次点击不踩雷。顶部有雷数计数器/笑脸重置/计时器，CSS Grid布局，响应式设计。额外：双击快速翻开、问号标记、localStorage最高分、Web Audio API音效。单文件零依赖，注释清晰兼容主流浏览器。工作流：分析需求→设计架构→编写代码→自测验证→review审查→安全检查→结项。输出 minesweeper.html。$cacheBuster"

# --max-steps 10 确保多智能体工作流有足够轮次执行
# --show-thinking  方便排查模型是否真的在调工具还是只输出文字
& "C:\Users\86183\AppData\Local\Programs\Reasonix\reasonix.exe" run --max-steps 10 --show-thinking $task

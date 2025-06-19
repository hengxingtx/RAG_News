import React, { useState, useEffect, useRef } from 'react';
import { Form, Input, Button, Card, message, Typography } from 'antd';
import { UserOutlined, LockOutlined, GlobalOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import './Login.css';
import './LoginOverride.css'; // 导入专门用于覆盖Ant Design样式的CSS

const { Title, Text } = Typography;

interface LoginForm {
    username: string;
    password: string;
}

// API基础URL
const API_BASE_URL = 'http://localhost:8007';

const Login: React.FC = () => {
    const [loading, setLoading] = useState(false);
    const [currentTime, setCurrentTime] = useState(new Date());
    const navigate = useNavigate();
    const usernameInputRef = useRef<any>(null);
    const passwordInputRef = useRef<any>(null);

    // 每秒更新一次时间
    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentTime(new Date());
        }, 1000);

        // 确保样式正确加载
        const link = document.createElement('link');
        link.href = `${window.location.origin}/src/pages/Login.css?v=${Date.now()}`;
        link.rel = 'stylesheet';
        link.type = 'text/css';
        document.head.appendChild(link);

        return () => {
            clearInterval(timer);
            document.head.removeChild(link);
        };
    }, []);

    // 专门处理从其他页面返回时的样式
    useEffect(() => {
        // 当组件挂载或重新渲染时检查和修复样式
        const applyStyles = () => {
            // 短暂延迟以确保DOM已完全加载
            setTimeout(() => {
                const fixBackgrounds = () => {
                    // 查找所有输入框并设置其背景色为白色
                    const allInputs = document.querySelectorAll('.login-form .ant-input, .login-form .ant-input-affix-wrapper');
                    allInputs.forEach((input) => {
                        if (input instanceof HTMLElement) {
                            input.style.setProperty('background-color', '#ffffff', 'important');
                            input.style.setProperty('background', '#ffffff', 'important');
                        }
                    });
                };

                // 立即应用一次
                fixBackgrounds();

                // 然后延迟再应用几次，确保在DOM更新后样式仍然正确
                setTimeout(fixBackgrounds, 100);
                setTimeout(fixBackgrounds, 500);
                setTimeout(fixBackgrounds, 1000);
            }, 50);
        };

        // 页面加载时应用样式
        applyStyles();

        // 页面获得焦点时重新应用样式
        window.addEventListener('focus', applyStyles);

        // 清理
        return () => {
            window.removeEventListener('focus', applyStyles);
        };
    }, []);

    // 保持输入框背景色为白色
    useEffect(() => {
        // 修复输入框背景色的函数
        const fixInputBackground = () => {
            // 修复输入框背景色
            const inputs = document.querySelectorAll<HTMLElement>('.login-form .ant-input, .login-form .ant-input-affix-wrapper');
            inputs.forEach(input => {
                input.style.backgroundColor = '#ffffff';
                input.style.background = '#ffffff';
            });
        };

        // 初始设置
        fixInputBackground();

        // 创建MutationObserver监视DOM变化
        const observer = new MutationObserver((mutations) => {
            fixInputBackground();
        });

        // 开始观察文档中与登录表单相关的部分
        const loginForm = document.querySelector('.login-form');
        if (loginForm) {
            observer.observe(loginForm, {
                childList: true,
                subtree: true,
                attributes: true,
                attributeFilter: ['style', 'class']
            });
        }

        // 每隔一段时间检查一次并修复
        const interval = setInterval(fixInputBackground, 300);

        // 组件卸载时清理
        return () => {
            clearInterval(interval);
            observer.disconnect();
        };
    }, []);

    // 处理输入框失去焦点事件
    const handleInputBlur = (e: React.FocusEvent<HTMLInputElement>) => {
        e.target.style.backgroundColor = '#ffffff';
        e.target.style.background = '#ffffff';

        // 如果是包含前缀的输入框，需要修复容器
        const wrapper = e.target.closest('.ant-input-affix-wrapper') as HTMLElement;
        if (wrapper) {
            wrapper.style.backgroundColor = '#ffffff';
            wrapper.style.background = '#ffffff';
        }
    };

    const onFinish = async (values: LoginForm) => {
        try {
            setLoading(true);
            console.log('登录信息:', values);

            // 调用后端登录API
            const formData = new URLSearchParams();
            formData.append('username', values.username);
            formData.append('password', values.password);

            const response = await fetch(`${API_BASE_URL}/api/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                message.success('登录成功！正在跳转...');

                // 保存token到本地存储
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('token_type', data.token_type);

                // 跳转到智能写作页面
                navigate('/writing');
            } else {
                // 处理不同的错误情况
                if (response.status === 401) {
                    message.error('用户名或密码错误，请重试');
                } else {
                    message.error(data.detail || '登录失败，请重试');
                }

                console.error('登录响应错误:', data);
            }
        } catch (error) {
            console.error('登录出错:', error);
            message.error('服务器连接失败，请确保后端服务器已启动');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            {/* 左侧大图区域 */}
            <div className="login-left">
                <img
                    src="/images/login-background.jpg"
                    alt="RAG News"
                    className="login-image"
                />
                <div className="login-image-overlay"></div>
            </div>

            {/* 右侧登录区域 */}
            <div className="login-right">
                <div className="login-decoration"></div>
                <div className="login-right-bg"></div>
                <div className="login-header">
                    <h1 className="art-title-game">RAG NEWS</h1>
                    <Text className="login-subtitle">智能新闻写作系统</Text>
                </div>

                <Card className="login-card" bordered={false}>
                    <div className="tech-info">
                        <div className="tech-time">
                            <GlobalOutlined className="tech-icon" />
                            <span>
                                {currentTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </span>
                        </div>
                        <div className="tech-status">
                            <span className="status-dot"></span>
                            <Text className="status-text">系统在线</Text>
                        </div>
                    </div>

                    <Form
                        name="login"
                        initialValues={{ remember: true }}
                        onFinish={onFinish}
                        size="large"
                        className="login-form"
                    >
                        <Form.Item
                            name="username"
                            rules={[{ required: true, message: '请输入用户名!' }]}
                            className="login-form-item"
                        >
                            <Input
                                prefix={<UserOutlined className="form-icon" />}
                                placeholder="用户名"
                                className="login-input white-bg-input"
                                style={{
                                    backgroundColor: '#ffffff',
                                    background: '#ffffff'
                                }}
                                ref={usernameInputRef}
                                onBlur={handleInputBlur}
                            />
                        </Form.Item>

                        <Form.Item
                            name="password"
                            rules={[{ required: true, message: '请输入密码!' }]}
                            className="login-form-item"
                        >
                            <Input.Password
                                prefix={<LockOutlined className="form-icon" />}
                                placeholder="密码"
                                className="login-input white-bg-input"
                                style={{
                                    backgroundColor: '#ffffff',
                                    background: '#ffffff'
                                }}
                                ref={passwordInputRef}
                                onBlur={handleInputBlur}
                            />
                        </Form.Item>

                        <Form.Item>
                            <Button
                                type="primary"
                                htmlType="submit"
                                className="login-button"
                                loading={loading}
                            >
                                登录系统
                            </Button>
                        </Form.Item>
                    </Form>
                </Card>
            </div>
        </div>
    );
};

export default Login; 
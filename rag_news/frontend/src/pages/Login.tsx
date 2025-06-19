import React, { useState, useEffect } from 'react';
import { Form, Input, Button, Card, message, Typography } from 'antd';
import { UserOutlined, LockOutlined, GlobalOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import './Login.css';

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
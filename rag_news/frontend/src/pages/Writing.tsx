import React, { useState } from 'react';
import { Layout, Menu, Button, Input, Card, Typography, Select, message } from 'antd';
import { EditOutlined, SendOutlined, FileTextOutlined, UserOutlined, LogoutOutlined, DatabaseOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import './Writing.css';

const { Header, Content, Sider } = Layout;
const { TextArea } = Input;
const { Title, Paragraph } = Typography;
const { Option } = Select;

const Writing: React.FC = () => {
    const navigate = useNavigate();
    const [prompt, setPrompt] = useState('');
    const [generatedContent, setGeneratedContent] = useState('');
    const [generating, setGenerating] = useState(false);
    const [contentType, setContentType] = useState('article');

    // 用户信息从本地存储中获取
    const token = localStorage.getItem('token');

    // 如果没有token，重定向到登录页面
    if (!token) {
        navigate('/');
        return null;
    }

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('token_type');
        navigate('/');
        message.success('已成功退出登录');
    };

    const handleGenerate = async () => {
        if (!prompt.trim()) {
            message.warning('请输入写作提示');
            return;
        }

        try {
            setGenerating(true);

            // 模拟生成内容
            setTimeout(() => {
                let generatedText = '';
                switch (contentType) {
                    case 'article':
                        generatedText = `# ${prompt}\n\n这是一篇关于${prompt}的文章...\n\n## 引言\n\n随着时代的发展，${prompt}的重要性日益凸显...`;
                        break;
                    case 'news':
                        generatedText = `# 最新消息：${prompt}\n\n据可靠消息，${prompt}相关事件正在迅速发展...`;
                        break;
                    default:
                        generatedText = `关于${prompt}的内容生成完成...`;
                }

                setGeneratedContent(generatedText);
                setGenerating(false);
                message.success('内容生成成功！');
            }, 1500);

            // 实际项目中，这里应该调用后端API
            // const response = await fetch(`${API_BASE_URL}/api/generate`, {
            //     method: 'POST',
            //     headers: {
            //         'Content-Type': 'application/json',
            //         'Authorization': `Bearer ${token}`
            //     },
            //     body: JSON.stringify({
            //         prompt,
            //         contentType
            //     })
            // });
            // 
            // const data = await response.json();
            // if (response.ok) {
            //     setGeneratedContent(data.content);
            //     message.success('内容生成成功！');
            // } else {
            //     message.error(data.detail || '生成内容失败');
            // }
        } catch (error) {
            console.error('生成内容出错:', error);
            message.error('生成请求失败，请稍后重试');
        } finally {
            setGenerating(false);
        }
    };

    return (
        <Layout style={{ minHeight: '100vh' }}>
            <Header style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                background: 'linear-gradient(to right, #0f5e9c, #2bb5f4)'
            }}>
                <div className="logo" style={{ color: 'white', fontSize: '20px', fontWeight: 'bold' }}>
                    RAG News 智能写作
                </div>
                <div style={{ display: 'flex', alignItems: 'center' }}>
                    <Button
                        type="text"
                        icon={<UserOutlined />}
                        style={{ color: 'white' }}
                    >
                        管理员
                    </Button>
                    <Button
                        type="text"
                        icon={<LogoutOutlined />}
                        onClick={handleLogout}
                        style={{ color: 'white' }}
                    >
                        退出
                    </Button>
                </div>
            </Header>
            <Layout>
                <Sider width={200} style={{ background: '#fff' }}>
                    <Menu
                        mode="inline"
                        defaultSelectedKeys={['writing']}
                        style={{ height: '100%', borderRight: 0 }}
                    >
                        <Menu.Item key="knowledge-base" icon={<DatabaseOutlined />} onClick={() => navigate('/knowledge-base')}>
                            知识库管理
                        </Menu.Item>
                        <Menu.Item key="writing" icon={<EditOutlined />}>
                            智能写作
                        </Menu.Item>
                        <Menu.Item key="history" icon={<FileTextOutlined />}>
                            历史记录
                        </Menu.Item>
                    </Menu>
                </Sider>
                <Layout style={{ padding: '24px' }}>
                    <Content style={{ background: '#fff', padding: 24, margin: 0, minHeight: 280 }}>
                        <Card title="智能写作" style={{ marginBottom: 20 }}>
                            <div style={{ marginBottom: 16 }}>
                                <Select
                                    value={contentType}
                                    onChange={(value) => setContentType(value)}
                                    style={{ width: 150, marginRight: 16 }}
                                >
                                    <Option value="article">文章</Option>
                                    <Option value="news">新闻</Option>
                                    <Option value="summary">摘要</Option>
                                </Select>
                                <span>选择您要生成的内容类型</span>
                            </div>
                            <TextArea
                                rows={4}
                                placeholder="请输入写作提示，例如：'关于人工智能在医疗领域的应用'"
                                value={prompt}
                                onChange={(e) => setPrompt(e.target.value)}
                                style={{ marginBottom: 16 }}
                            />
                            <Button
                                type="primary"
                                icon={<SendOutlined />}
                                loading={generating}
                                onClick={handleGenerate}
                                className="generate-btn"
                                style={{
                                    background: 'linear-gradient(45deg, #0f5e9c, #2bb5f4)',
                                    border: 'none'
                                }}
                            >
                                开始生成
                            </Button>
                        </Card>

                        {generatedContent && (
                            <Card title="生成结果" className="result-card">
                                <div className="generated-result" style={{ whiteSpace: 'pre-wrap' }}>
                                    {generatedContent}
                                </div>
                            </Card>
                        )}
                    </Content>
                </Layout>
            </Layout>
        </Layout>
    );
};

export default Writing; 
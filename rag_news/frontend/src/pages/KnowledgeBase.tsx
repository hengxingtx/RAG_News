import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Layout, Menu, Button, message } from 'antd';
import { EditOutlined, DatabaseOutlined, FileTextOutlined, UserOutlined, LogoutOutlined } from '@ant-design/icons';
import './KnowledgeBase.css';

const { Header, Content, Sider } = Layout;

interface KnowledgeBase {
    id: number;
    name: string;
    description: string | null;
    created_at: string;
    updated_at: string;
    file_count: number;
}

interface KnowledgeFile {
    id: number;
    filename: string;
    original_filename: string;
    file_type: string;
    file_size: number;
    status: string;
    created_at: string;
}

const KnowledgeBasePage: React.FC = () => {
    const [knowledgeBases, setKnowledgeBases] = useState<KnowledgeBase[]>([]);
    const [selectedKb, setSelectedKb] = useState<KnowledgeBase | null>(null);
    const [files, setFiles] = useState<KnowledgeFile[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [newKbName, setNewKbName] = useState<string>('');
    const [newKbDescription, setNewKbDescription] = useState<string>('');
    const [showCreateForm, setShowCreateForm] = useState<boolean>(false);
    const [uploadingFile, setUploadingFile] = useState<boolean>(false);
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('token_type');
        navigate('/');
        message.success('已成功退出登录');
    };

    const fetchKnowledgeBases = async () => {
        console.log("开始获取知识库列表");
        setIsLoading(true);
        setError(null);
        try {
            const token = localStorage.getItem('token');
            console.log("Token是否存在:", !!token);

            if (!token) {
                navigate('/');
                return;
            }

            console.log("发送API请求到:", '/api/knowledge-base/');
            const response = await axios.get('/api/knowledge-base/', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            console.log("获取到知识库列表:", response.data);
            setKnowledgeBases(response.data);
        } catch (err: any) {
            console.error("获取知识库列表失败:", err);
            const errorMessage = err.response?.data?.detail || '获取知识库列表失败';
            setError(errorMessage);
        } finally {
            setIsLoading(false);
        }
    };

    const fetchKnowledgeBaseFiles = async (kbId: number) => {
        setIsLoading(true);
        setError(null);
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/');
                return;
            }

            const response = await axios.get(`/api/knowledge-base/${kbId}/files`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            console.log("获取到文件列表:", response.data);
            setFiles(response.data);
        } catch (err: any) {
            console.error("获取文件列表失败:", err);
            const errorMessage = err.response?.data?.detail || '获取文件列表失败';
            setError(errorMessage);
        } finally {
            setIsLoading(false);
        }
    };

    const handleCreateKnowledgeBase = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null);
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/');
                return;
            }

            console.log("创建知识库:", { name: newKbName, description: newKbDescription });
            await axios.post('/api/knowledge-base/', {
                name: newKbName,
                description: newKbDescription || null
            }, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            setNewKbName('');
            setNewKbDescription('');
            setShowCreateForm(false);
            fetchKnowledgeBases();
        } catch (err: any) {
            console.error("创建知识库失败:", err);
            const errorMessage = err.response?.data?.detail || '创建知识库失败';
            setError(errorMessage);
        } finally {
            setIsLoading(false);
        }
    };

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>, kbId: number) => {
        if (!e.target.files || e.target.files.length === 0) return;

        setUploadingFile(true);
        setError(null);
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/');
                return;
            }

            const formData = new FormData();
            formData.append('file', e.target.files[0]);

            console.log("上传文件到知识库:", kbId);
            await axios.post(`/api/knowledge-base/${kbId}/upload`, formData, {
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'multipart/form-data'
                }
            });

            fetchKnowledgeBaseFiles(kbId);
        } catch (err: any) {
            console.error("上传文件失败:", err);
            const errorMessage = err.response?.data?.detail || '上传文件失败';
            setError(errorMessage);
        } finally {
            setUploadingFile(false);
            e.target.value = '';
        }
    };

    const handleDeleteFile = async (kbId: number, fileId: number) => {
        if (!window.confirm('确定要删除此文件吗？')) return;

        setIsLoading(true);
        setError(null);
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/');
                return;
            }

            await axios.delete(`/api/knowledge-base/${kbId}/files/${fileId}`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            fetchKnowledgeBaseFiles(kbId);
        } catch (err: any) {
            console.error("删除文件失败:", err);
            const errorMessage = err.response?.data?.detail || '删除文件失败';
            setError(errorMessage);
        } finally {
            setIsLoading(false);
        }
    };

    const handleDeleteKnowledgeBase = async (kbId: number) => {
        if (!window.confirm('确定要删除此知识库吗？所有相关文件也将被删除。')) return;

        setIsLoading(true);
        setError(null);
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/');
                return;
            }

            await axios.delete(`/api/knowledge-base/${kbId}`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            setSelectedKb(null);
            setFiles([]);
            fetchKnowledgeBases();
        } catch (err: any) {
            console.error("删除知识库失败:", err);
            const errorMessage = err.response?.data?.detail || '删除知识库失败';
            setError(errorMessage);
        } finally {
            setIsLoading(false);
        }
    };

    const selectKnowledgeBase = (kb: KnowledgeBase) => {
        setSelectedKb(kb);
        fetchKnowledgeBaseFiles(kb.id);
    };

    const formatFileSize = (bytes: number) => {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    };

    useEffect(() => {
        console.log("KnowledgeBasePage组件加载");
        fetchKnowledgeBases();
    }, []);

    console.log("渲染KnowledgeBasePage组件, 状态:", {
        knowledgeBaseCount: knowledgeBases.length,
        isLoading,
        hasError: !!error
    });

    return (
        <Layout style={{ minHeight: '100vh' }}>
            <Header style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                background: 'linear-gradient(to right, #0f5e9c, #2bb5f4)'
            }}>
                <div className="logo" style={{ color: 'white', fontSize: '20px', fontWeight: 'bold' }}>
                    RAG News 知识库管理
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
                        defaultSelectedKeys={['knowledge-base']}
                        style={{ height: '100%', borderRight: 0 }}
                    >
                        <Menu.Item key="knowledge-base" icon={<DatabaseOutlined />}>
                            知识库管理
                        </Menu.Item>
                        <Menu.Item key="writing" icon={<EditOutlined />} onClick={() => navigate('/writing')}>
                            智能写作
                        </Menu.Item>
                        <Menu.Item key="history" icon={<FileTextOutlined />}>
                            历史记录
                        </Menu.Item>
                    </Menu>
                </Sider>
                <Layout style={{ padding: '24px' }}>
                    <Content style={{ background: '#fff', padding: 24, margin: 0, minHeight: 280 }}>
                        <div className="knowledge-base-container">
                            <div className="knowledge-base-header">
                                <h1>知识库管理</h1>
                                <button
                                    className="create-kb-btn"
                                    onClick={() => setShowCreateForm(!showCreateForm)}
                                >
                                    {showCreateForm ? '取消' : '创建知识库'}
                                </button>
                            </div>

                            {error && <div className="error-message">{error}</div>}

                            {showCreateForm && (
                                <div className="create-kb-form">
                                    <form onSubmit={handleCreateKnowledgeBase}>
                                        <div className="form-group">
                                            <label htmlFor="kb-name">知识库名称：</label>
                                            <input
                                                type="text"
                                                id="kb-name"
                                                value={newKbName}
                                                onChange={(e) => setNewKbName(e.target.value)}
                                                required
                                                placeholder="输入知识库名称"
                                            />
                                        </div>
                                        <div className="form-group">
                                            <label htmlFor="kb-description">知识库描述：</label>
                                            <textarea
                                                id="kb-description"
                                                value={newKbDescription}
                                                onChange={(e) => setNewKbDescription(e.target.value)}
                                                placeholder="输入知识库描述（可选）"
                                            />
                                        </div>
                                        <button type="submit" disabled={isLoading}>
                                            {isLoading ? '创建中...' : '创建知识库'}
                                        </button>
                                    </form>
                                </div>
                            )}

                            <div className="knowledge-base-content">
                                <div className="kb-list">
                                    <h2>知识库列表</h2>
                                    {isLoading && !selectedKb && <div className="loading">加载中...</div>}
                                    {knowledgeBases.length === 0 && !isLoading ? (
                                        <div className="empty-message">暂无知识库，请创建一个新的知识库。</div>
                                    ) : (
                                        <ul>
                                            {knowledgeBases.map((kb) => (
                                                <li
                                                    key={kb.id}
                                                    className={selectedKb?.id === kb.id ? 'selected' : ''}
                                                    onClick={() => selectKnowledgeBase(kb)}
                                                >
                                                    <div className="kb-name">{kb.name}</div>
                                                    <div className="kb-file-count">{kb.file_count} 个文件</div>
                                                </li>
                                            ))}
                                        </ul>
                                    )}
                                </div>

                                {selectedKb && (
                                    <div className="kb-detail">
                                        <div className="kb-detail-header">
                                            <h2>{selectedKb.name}</h2>
                                            <div className="kb-actions">
                                                <label className="upload-file-btn">
                                                    上传文件
                                                    <input
                                                        type="file"
                                                        onChange={(e) => handleFileUpload(e, selectedKb.id)}
                                                        disabled={uploadingFile}
                                                        style={{ display: 'none' }}
                                                    />
                                                </label>
                                                <button
                                                    className="delete-kb-btn"
                                                    onClick={() => handleDeleteKnowledgeBase(selectedKb.id)}
                                                    disabled={isLoading}
                                                >
                                                    删除知识库
                                                </button>
                                            </div>
                                        </div>

                                        {selectedKb.description && (
                                            <div className="kb-description">{selectedKb.description}</div>
                                        )}

                                        <div className="kb-files">
                                            <h3>文件列表</h3>
                                            {isLoading && <div className="loading">加载中...</div>}
                                            {files.length === 0 && !isLoading ? (
                                                <div className="empty-message">暂无文件，请上传文件。</div>
                                            ) : (
                                                <table>
                                                    <thead>
                                                        <tr>
                                                            <th>文件名</th>
                                                            <th>类型</th>
                                                            <th>大小</th>
                                                            <th>状态</th>
                                                            <th>上传时间</th>
                                                            <th>操作</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        {files.map((file) => (
                                                            <tr key={file.id}>
                                                                <td>{file.original_filename}</td>
                                                                <td>{file.file_type}</td>
                                                                <td>{formatFileSize(file.file_size)}</td>
                                                                <td>
                                                                    <span className={`status-${file.status}`}>
                                                                        {file.status === 'pending' && '待处理'}
                                                                        {file.status === 'processing' && '处理中'}
                                                                        {file.status === 'completed' && '已完成'}
                                                                        {file.status === 'error' && '错误'}
                                                                    </span>
                                                                </td>
                                                                <td>{new Date(file.created_at).toLocaleString()}</td>
                                                                <td>
                                                                    <button
                                                                        className="delete-file-btn"
                                                                        onClick={() => handleDeleteFile(selectedKb.id, file.id)}
                                                                        disabled={isLoading}
                                                                    >
                                                                        删除
                                                                    </button>
                                                                </td>
                                                            </tr>
                                                        ))}
                                                    </tbody>
                                                </table>
                                            )}
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    </Content>
                </Layout>
            </Layout>
        </Layout>
    );
};

export default KnowledgeBasePage; 
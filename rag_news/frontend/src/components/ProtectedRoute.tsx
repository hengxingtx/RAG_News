import { Navigate, useLocation } from 'react-router-dom';

interface ProtectedRouteProps {
    children: React.ReactNode;
}

const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
    const location = useLocation();
    const token = localStorage.getItem('token');

    if (!token) {
        // 如果没有登录，重定向到登录页面
        return <Navigate to="/" state={{ from: location }} replace />;
    }

    // 如果已登录，渲染子组件
    return <>{children}</>;
};

export default ProtectedRoute; 
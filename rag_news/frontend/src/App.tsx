import { Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Writing from './pages/Writing';
import KnowledgeBase from './pages/KnowledgeBase';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
    return (
        <Routes>
            <Route path="/" element={<Login />} />
            <Route
                path="/knowledge-base"
                element={
                    <ProtectedRoute>
                        <KnowledgeBase />
                    </ProtectedRoute>
                }
            />
            <Route
                path="/writing"
                element={
                    <ProtectedRoute>
                        <Writing />
                    </ProtectedRoute>
                }
            />
            <Route path="*" element={<Login />} />
        </Routes>
    );
}

export default App; 
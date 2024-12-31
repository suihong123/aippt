interface User {
    id: string;
    phone: string;
    create_time: number;
    last_login: number;
    status: 'active' | 'inactive';
}

interface ActivationCode {
    code: string;
    status: 'unused' | 'used' | 'expired';
    create_time: number;
    use_time?: number;
    remaining_uses: number;
    expire_time: number;
}

interface UsageStats {
    remaining_uses: number;
    expire_time: number;
    used_count: number;
}

interface APIResponse<T> {
    success: boolean;
    message?: string;
    data?: T;
} 
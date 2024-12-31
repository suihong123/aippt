const ENV = {
    development: {
        API_BASE_URL: 'http://localhost:3000',
        DEBUG: true
    },
    production: {
        API_BASE_URL: 'https://api.docmee.cn',
        DEBUG: false
    }
};

const currentEnv = process.env.NODE_ENV || 'development';
export default ENV[currentEnv]; 
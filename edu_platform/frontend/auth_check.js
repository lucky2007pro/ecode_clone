// auth_check.js
// This script checks if the user is authenticated. 
// Include it in the <head> of protected pages: <script src="/auth_check.js"></script>

(function() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login';
        return;
    }
    
    // Optional: parse JWT and check expiration
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join(''));
        const payload = JSON.parse(jsonPayload);
        
        const now = Math.floor(Date.now() / 1000);
        if (payload.exp < now) {
            localStorage.removeItem('access_token');
            window.location.href = '/login';
        }
    } catch(e) {
        localStorage.removeItem('access_token');
        window.location.href = '/login';
    }
})();

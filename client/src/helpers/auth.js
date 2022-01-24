import axios from 'axios';
import { config } from './constants';

export const checkAuthenticated = () => {
    const accessToken = localStorage.getItem('access token');
    const refreshToken = localStorage.getItem('refresh token');

    if (accessToken && refreshToken) {
        return true;
    }
    return false;
}

export const refreshAccessToken = async () => {
    const refreshToken = localStorage.getItem('refresh token');
    try {
        const { data } = await axios.post(`${config.httpProtocol}://${config.serverDomain}/token/refresh/`, {
            'refresh': refreshToken
        });
        const newAccessToken = data.access;
        localStorage.setItem('access token', newAccessToken);
        return newAccessToken;
    } catch (err) {
        return null;
    }
}

export const signIn = async (email, password) => {
    try {
        const { data } = await axios.post(`${config.httpProtocol}://${config.serverDomain}/token/`, {
            email,
            password
        });

        const accessToken = data.access;
        const refreshToken = data.refresh;

        localStorage.setItem('access token', accessToken);
        localStorage.setItem('refresh token', refreshToken);

        return true;
    } catch (err) {
        return false
    }
}

export const signOut = () => {
    localStorage.removeItem('access token');
    localStorage.removeItem('refresh token');
}
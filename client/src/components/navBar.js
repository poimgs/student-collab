import axios from 'axios';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import AppBar from '@mui/material/AppBar';
import Menu from '@mui/material/Menu';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import { refreshAccessToken, signOut } from '../helpers/auth';
import { config } from '../helpers/constants';

const NavBar = () => {
    const navigate = useNavigate();

    const [anchorElRooms, setAnchorElRooms] = useState(null);
    const [rooms, setRooms] = useState([]);

    const handleOpenRoomsMenu = (e) => {
        setAnchorElRooms(e.currentTarget);
    };

    const handleCloseRoomsMenu = (e) => {
        setAnchorElRooms(null);
    };

    const handleMenuItemClick = (path) => {
        setAnchorElRooms(null);
        navigate(path);
    }

    const handleLogOutButtonClick = () => {
        signOut();
        navigate('/signIn');
    }

    useEffect(() => {
        const source = axios.CancelToken.source();

        const getRoomsInfo = async () => {
            const accessToken = localStorage.getItem('access token');
            const httpURL = `${config.httpProtocol}://${config.serverDomain}/discussion/rooms/`;

            try {
                const data = await axios.get(httpURL, {
                    headers: { 'Authorization': `Bearer ${accessToken}` },
                    cancelToken: source.token,
                });
                setRooms(data.data)
            } catch (err) {
                if (err.response.data.code === 'token_not_valid') {
                    const newAccessToken = await refreshAccessToken();
                    if (newAccessToken) {
                        const data = await axios.get(httpURL, {
                            headers: { 'Authorization': `Bearer ${accessToken}` },
                            cancelToken: source.token,
                        });
                        setRooms(data.data);
                    } else {
                        signOut();
                        navigate('/signIn');
                    }
                }
            }
        }

        getRoomsInfo();

        return () => {
            source.cancel();
        }
    }, [])

    return (
        <AppBar color='primary'>
            <Toolbar>
                <Button
                    color='inherit'
                    size='large'
                    sx={{ mr: 'auto' }}
                    onClick={() => navigate('/')}
                >
                    Student Collab
                </Button>
                <Box>
                    <Tooltip title="Navigate to different rooms">
                        <Button onClick={handleOpenRoomsMenu} color='inherit'>
                            Rooms
                        </Button>
                    </Tooltip>
                    <Menu
                        anchorEl={anchorElRooms}
                        open={Boolean(anchorElRooms)}
                        onClose={handleCloseRoomsMenu}
                    >
                        {rooms.map((roomInfo, index) => {
                            const moduleName = roomInfo.module;
                            const id = roomInfo.id;
                            const path = '/' + id;

                            return (
                                <MenuItem
                                    key={index}
                                    onClick={() => handleMenuItemClick(path)}
                                >
                                    <Typography textAlign="center">{moduleName}</Typography>
                                </MenuItem>
                            )
                        })}
                    </Menu>
                </Box>
                <Button
                    color='inherit'
                    onClick={() => handleLogOutButtonClick()}
                >
                    Logout
                </Button>
            </Toolbar >
        </AppBar >
    );
}

export default NavBar;
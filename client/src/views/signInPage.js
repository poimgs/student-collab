import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Alert from '@mui/material/Alert';
import { signIn } from '../helpers/auth';

const SignInPage = () => {
    const [signInFailed, setSignInFailed] = useState(false);
    const location = useLocation();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = new FormData(e.currentTarget);
        const email = data.get('email');
        const password = data.get('password');
        const signedIn = await signIn(email, password);

        if (!signedIn) {
            setSignInFailed(true);
        } else {
            if (location.state) {
                navigate(location.state.from);
            } else {
                navigate('/');
            }
        }
    }

    return (
        <Container maxWidth='xs' sx={{ marginTop: 12 }}>
            <Typography variant='h4' align='center'>
                Sign in
            </Typography>
            <Box component='form' onSubmit={handleSubmit}>
                <TextField
                    margin="normal"
                    required
                    fullWidth
                    id="email"
                    label="Email Address"
                    name="email"
                    autoComplete="email"
                    autoFocus
                />
                <TextField
                    margin="normal"
                    required
                    fullWidth
                    id="password"
                    label="Password"
                    name="password"
                    type="password"
                    autoComplete="current-password"
                />
                <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    sx={{ mt: 3, mb: 2 }}
                >
                    Sign In
                </Button>
                {signInFailed ? (
                    <Alert severity="error">
                        Invalid credentials entered
                    </Alert>
                ) : null}
            </Box>
        </Container>
    )
}

export default SignInPage;
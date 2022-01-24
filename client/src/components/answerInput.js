import Container from '@mui/material/Container';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';
import { useState } from 'react';

const AnswerInput = ({ question_id, handleAnswerInputEnter }) => {
    const [inputValue, setInputValue] = useState('')

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    }

    const handleButtonClick = (e) => {
        if (inputValue.trim().length > 0) {
            handleAnswerInputEnter(inputValue, question_id);
            setInputValue('');
        }
    }

    return (
        <Container >
            <TextField
                label="Your Input"
                multiline
                fullWidth
                margin="normal"
                minRows={4}
                maxRows={50}
                value={inputValue}
                onChange={handleInputChange}
            />
            <Button
                variant="contained"
                fullWidth
                endIcon={<SendIcon />}
                sx={{ marginBottom: 1 }}
                onClick={(e) => handleButtonClick(e)}
            >
                Send
            </Button>
        </Container>
    )
}

export default AnswerInput;
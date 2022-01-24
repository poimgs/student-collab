import TextField from '@mui/material/TextField';
import { useState } from 'react';

const QuestionInput = ({ handleQuestionInputEnter }) => {
    const [inputValue, setInputValue] = useState('')

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && inputValue.length > 0) {
            handleQuestionInputEnter(inputValue);
            setInputValue('');
        }
    }

    return (
        <TextField
            label="My Question"
            fullWidth
            margin="normal"
            helperText="Press Enter to Submit"
            value={inputValue}
            onChange={handleInputChange}
            onKeyDown={(e) => handleKeyDown(e)}
        />
    )
}

export default QuestionInput;
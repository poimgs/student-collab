import Box from "@mui/material/Box";
import Question from "./question";

const Questions = ({ questions, handleAnswerInputEnter, handleQuestionUpvoteButtonClick }) => {
    if (questions) {
        return (
            <Box>
                {questions.map((questionInfo) => {
                    return (
                        <Question
                            key={questionInfo.id}
                            questionInfo={questionInfo}
                            handleAnswerInputEnter={handleAnswerInputEnter}
                            handleQuestionUpvoteButtonClick={handleQuestionUpvoteButtonClick}
                        />
                    )
                })}
            </Box>
        )
    } else {
        return (
            null
        )
    }

}

export default Questions;


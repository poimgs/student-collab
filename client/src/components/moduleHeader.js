import Typography from '@mui/material/Typography';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import Badge from '@mui/material/Badge';

const ModuleHeader = ({ moduleName, isLost, numLost, handleIsLostButtonClick }) => {
    return (
        <Typography variant='h3' align='center' mt={11}>
            {moduleName}
            <Tooltip title='Click me if you are lost and do not know what question to ask'>
                <IconButton onClick={() => handleIsLostButtonClick(!isLost)}>
                    <Badge
                        badgeContent={numLost}
                        color="error"
                        fontSize='large'
                    >
                        <HelpOutlineIcon fontSize='large' color={isLost ? 'primary' : undefined} />
                    </Badge>
                </IconButton>
            </Tooltip>
        </Typography>
    )
}

export default ModuleHeader;
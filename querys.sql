CREATE DATABASE parking;

CREATE TABLE parking.space (
    floor INT NOT NULL,
    spot CHAR NOT NULL,
    used BOOL DEFAULT TRUE,
    PRIMARY KEY (floor, space)
);

#EXAMPLES
INSERT INTO `parking`.`space` (`floor`, `spot`, `used`) VALUES ('0', 'A', '0');
INSERT INTO `parking`.`space` (`floor`, `spot`, `used`) VALUES ('0', 'B', '0');
INSERT INTO `parking`.`space` (`floor`, `spot`, `used`) VALUES ('0', 'C', '0');
INSERT INTO `parking`.`space` (`floor`, `spot`, `used`) VALUES ('0', 'D', '0');
INSERT INTO `parking`.`space` (`floor`, `spot`, `used`) VALUES ('0', 'E', '0');
INSERT INTO `parking`.`space` (`floor`, `spot`, `used`) VALUES ('0', 'F', '0');
INSERT INTO `parking`.`space` (`floor`, `spot`, `used`) VALUES ('0', 'G', '0');
INSERT INTO `parking`.`space` (`floor`, `spot`, `used`) VALUES ('0', 'H', '0');

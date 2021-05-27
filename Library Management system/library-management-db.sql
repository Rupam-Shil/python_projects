-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 27, 2021 at 03:10 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `library-management-db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `User Name` varchar(200) NOT NULL,
  `Name` varchar(200) NOT NULL,
  `Password` varchar(200) NOT NULL,
  `Email` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`User Name`, `Name`, `Password`, `Email`) VALUES
('saira12', 'Saira Tabassum', '12345678', 'saira34@gmail.com'),
('saira23', 'saira tabassum', '1372173612', 'saira23@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `book_details`
--

CREATE TABLE `book_details` (
  `Book ID` int(11) NOT NULL,
  `Title` varchar(200) NOT NULL,
  `Author` varchar(200) NOT NULL,
  `Edition` int(11) NOT NULL,
  `Total` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `book_details`
--

INSERT INTO `book_details` (`Book ID`, `Title`, `Author`, `Edition`, `Total`) VALUES
(1001, 'Golpo Kotha', 'Humayun Ahmed', 2001, 9),
(1002, 'Twilight', 'Stephen Mayer', 2002, 14),
(1003, 'Flyover', 'A P J Abdul Kalam', 2003, 12),
(1004, 'Himu', 'Humayun Ahmed', 2004, 5),
(1005, 'Twilight Eclipse', 'Stephen Mayer', 2002, 21);

-- --------------------------------------------------------

--
-- Table structure for table `issue_information`
--

CREATE TABLE `issue_information` (
  `Issue ID` int(11) NOT NULL,
  `Std_ID` int(11) NOT NULL,
  `Book ID` int(11) NOT NULL,
  `From Date` varchar(200) NOT NULL,
  `To Date` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `issue_information`
--

INSERT INTO `issue_information` (`Issue ID`, `Std_ID`, `Book ID`, `From Date`, `To Date`) VALUES
(12, 1, 1001, '4/16/21', '4/16/21'),
(13, 1, 1001, '4/19/2021', '5/19/2021'),
(56, 1, 1003, '4/19/2021', '8/19/2021'),
(78, 1, 1001, '4/21/21', '4/21/21');

-- --------------------------------------------------------

--
-- Table structure for table `student_information`
--

CREATE TABLE `student_information` (
  `Std_ID` int(11) NOT NULL,
  `Name` varchar(200) NOT NULL,
  `Department` varchar(200) NOT NULL,
  `Year` int(11) NOT NULL,
  `Semester` varchar(200) NOT NULL,
  `Contact` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `student_information`
--

INSERT INTO `student_information` (`Std_ID`, `Name`, `Department`, `Year`, `Semester`, `Contact`) VALUES
(1, 'Saira Tabassum', 'CSE', 2019, '7', '0177272913');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`Password`);

--
-- Indexes for table `book_details`
--
ALTER TABLE `book_details`
  ADD PRIMARY KEY (`Book ID`);

--
-- Indexes for table `issue_information`
--
ALTER TABLE `issue_information`
  ADD PRIMARY KEY (`Issue ID`),
  ADD KEY `Std_ID` (`Std_ID`),
  ADD KEY `Book ID` (`Book ID`);

--
-- Indexes for table `student_information`
--
ALTER TABLE `student_information`
  ADD PRIMARY KEY (`Std_ID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `issue_information`
--
ALTER TABLE `issue_information`
  ADD CONSTRAINT `issue_information_ibfk_1` FOREIGN KEY (`Std_ID`) REFERENCES `student_information` (`Std_ID`),
  ADD CONSTRAINT `issue_information_ibfk_2` FOREIGN KEY (`Book ID`) REFERENCES `book_details` (`Book ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

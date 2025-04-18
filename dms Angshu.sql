-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 18, 2025 at 02:02 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dms`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `password`, `email`) VALUES
(1, '123', 'admin.01@gmail.com'),
(2, '456', 'admin.02@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `appointment`
--

CREATE TABLE `appointment` (
  `app_id` int(11) NOT NULL,
  `d_id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `time` time DEFAULT NULL,
  `confirmation` tinyint(1) NOT NULL DEFAULT 0,
  `checked` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appointment`
--

INSERT INTO `appointment` (`app_id`, `d_id`, `p_id`, `date`, `time`, `confirmation`, `checked`) VALUES
(1, 1, 1, '2024-09-18', '15:20:00', 1, 1),
(5, 2, 1, '2024-09-26', '18:00:00', 1, 1),
(6, 5, 1, '2024-09-23', '16:30:00', 0, 0),
(7, 4, 1, '2024-09-18', '17:30:00', 0, 0),
(8, 1, 1, '2024-09-19', '17:30:00', 0, 0),
(9, 1, 1, '2024-09-22', '15:00:00', 2, 0),
(10, 1, 1, '2024-09-25', '18:30:00', 1, 1),
(11, 1, 4, '2024-09-23', '18:00:00', 1, 1),
(12, 1, 5, '2024-09-22', '18:20:00', 0, 0),
(13, 4, 3, '2024-09-25', '18:20:00', 0, 0),
(14, 2, 1, '2024-09-30', '15:22:00', 0, 0),
(15, 10, 1, '2024-10-03', '17:15:00', 1, 1),
(16, 1, 1, '2024-10-07', '17:44:00', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `doctor`
--

CREATE TABLE `doctor` (
  `d_id` int(11) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `designation` varchar(255) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `verified` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doctor`
--

INSERT INTO `doctor` (`d_id`, `password`, `email`, `name`, `designation`, `phone`, `location`, `verified`) VALUES
(1, 'DMC', 'srar.74@gmail.com', 'Sultana Rehana Akhter', 'Deputy Chief Medical Officer, MBBS, CCD (BIRDEM)', '01711451490', 'OPD, BIRDEM General Hospital, Shahbag, Dhaka', 1),
(2, 'SSMC', 'imtiaz.69@gmail.com', 'Imtiaz Faruk', 'Professor, MBBS, FCPS, FRCS (Glasgow)', '01819231809', 'Dhaka Medical College and Hospital, Secretariat Road, Dhaka, Bangladesh', 1),
(3, 'RMC', 'habib@gmail.com', 'Habibul Isak', 'MBBS, FCPS, FRCS (Ed)', '01971451490', 'Samorita Hospital Limited\r\n89/1, Panthapath, Dhaka-1215, Bangladesh', 1),
(4, 'MMC', 'faruque@yahoo.com', 'Md Faruque Pathan', 'Professor, MBBS, MD (EM), FACE (USA)', '01777335056', 'BIRDEM,122 Kazi Nazrul Islam Avenue, Shahbagh, Dhaka 1000', 1),
(5, 'RMCH', 'motiur@gmail.com', 'Md. Motiur Rahman', 'Registrar (DM), MBBS, FCPS (Medicine), DEM (BIRDEM)', '01991674809', 'Square Provate Hospital, 18 Bir Uttam Qazi Nuruzzaman Sarak West, Panthapath, Dhaka 1205, Bangladesh', 1),
(6, 'SQUARE', 'pratik@yahoo.com', 'Pratik Dewan', 'Consultant (IME), MBBS, DEM, MD (Internal Medicine), BIRDEM Academy', '01752346567', 'Nafi Tower, Level-3 (2nd floor),\r\n53 Gulshan Avenue, Gulshan-1,\r\nDhaka- 1212', 1),
(7, '123', 'yan@gmail.com', 'Yan Ali', NULL, NULL, NULL, 1),
(8, 'mat216', 'hosan@gmail.com', 'Hosan Ali', NULL, NULL, NULL, 0),
(9, '123', 'admin.01@gmail.com', 'dsad', NULL, NULL, NULL, 0),
(10, '890', 'razia@gmail.com', 'Razia Akhter', 'Professor', '0187235210', 'Rmc', 1);

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

CREATE TABLE `patient` (
  `p_id` int(11) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `weight` decimal(5,2) DEFAULT NULL,
  `gender` enum('Male','Female','Other') DEFAULT NULL,
  `gl_b_breakfast` decimal(3,1) DEFAULT NULL,
  `gl_a_breakfast` decimal(3,1) DEFAULT NULL,
  `gl_b_lunch` decimal(3,1) DEFAULT NULL,
  `gl_b_dinner` decimal(3,1) DEFAULT NULL,
  `updated_on` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patient`
--

INSERT INTO `patient` (`p_id`, `password`, `email`, `name`, `dob`, `weight`, `gender`, `gl_b_breakfast`, `gl_a_breakfast`, `gl_b_lunch`, `gl_b_dinner`, `updated_on`) VALUES
(1, 'patient', 'jake@gmail.com', 'Sim Jake', '2002-11-15', 66.00, 'Male', 6.0, 11.7, 15.7, 11.8, '2025-04-13 14:08:53'),
(2, '098', 'aditya@gmail.com', 'Aditya', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2024-09-18 08:57:59'),
(3, 'na', 'nahian@gmail.com', 'nahian', '0000-00-00', 76.00, 'Female', 3.0, 6.0, 15.0, 30.0, '2024-09-21 20:06:51'),
(4, '123', 'labiba@gmail.com', 'labiba', '1999-07-19', 76.00, 'Female', 6.7, 5.0, 10.0, 17.0, '2024-09-19 11:39:13'),
(5, 'en30', 'jay@gmail.com', 'Jay', '1990-09-24', 100.00, 'Male', 6.0, 3.0, 2.0, 15.0, '2024-09-21 12:17:34');

-- --------------------------------------------------------

--
-- Table structure for table `prescription`
--

CREATE TABLE `prescription` (
  `pres_id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL,
  `d_id` int(11) NOT NULL,
  `detail` text DEFAULT NULL,
  `date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `prescription`
--

INSERT INTO `prescription` (`pres_id`, `p_id`, `d_id`, `detail`, `date`) VALUES
(1, 1, 1, 'Metformin, dose: (0 + 1 + 1)\r\nContinue it 15 days,  Empa Gliflozin, dose: (1 + 1 + 1) Continue it 1 month,  Suggested Diet Plan: 1', '2024-09-17'),
(2, 1, 2, 'Alpha-glucosidase inhibitor,\r\ndose: 1 + 1 + 1\r\n\r\nSuggested Diet Plan: \r\nFollow your current one', '2024-09-17'),
(3, 1, 6, 'Insulin (Morning: 10 unit) (After Dinner: 15 unit) ', '2024-09-17'),
(4, 1, 1, 'increase the dose of metformin, dose: 1+ 1+ 1 ', '2024-09-18'),
(5, 1, 1, 'Insulin 30mg', '2024-09-18'),
(6, 1, 1, 'daily walk for 1 hour a day. Maintain regularity.', '2024-09-18'),
(7, 1, 1, 'Increase the dose of Insulin', '2024-09-18'),
(8, 4, 1, 'Metformin dose decrease. dose: 1+ 0 + 1', '2024-09-19'),
(9, 1, 10, 'Increase the dose of insulin', '2024-09-29'),
(10, 1, 1, '- Diabetic diet, \r\n- exercise\r\n- Empa 10', '2024-10-04');

-- --------------------------------------------------------

--
-- Table structure for table `slot`
--

CREATE TABLE `slot` (
  `slot_id` int(11) NOT NULL,
  `slot_time` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `slot`
--

INSERT INTO `slot` (`slot_id`, `slot_time`) VALUES
(1, '15:00:00'),
(2, '15:30:00'),
(3, '16:00:00'),
(4, '16:30:00'),
(5, '17:00:00'),
(6, '17:30:00'),
(7, '18:00:00'),
(8, '18:30:00');

-- --------------------------------------------------------

--
-- Table structure for table `sos_alerts`
--

CREATE TABLE `sos_alerts` (
  `p_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sos_alerts`
--

INSERT INTO `sos_alerts` (`p_id`, `name`, `location`, `timestamp`) VALUES
(1, 'Sim Jake', '23.8007803,90.3613112', '2025-04-18 17:43:37'),
(2, 'Aditya', '23.8007803,90.3613112', '2025-04-18 17:53:04');

-- --------------------------------------------------------

--
-- Table structure for table `sugar_lvl`
--

CREATE TABLE `sugar_lvl` (
  `Food` varchar(20) NOT NULL,
  `Sugar_level` float(4,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sugar_lvl`
--

INSERT INTO `sugar_lvl` (`Food`, `Sugar_level`) VALUES
('Milk Shake', 15.89);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `appointment`
--
ALTER TABLE `appointment`
  ADD PRIMARY KEY (`app_id`),
  ADD KEY `d_id` (`d_id`),
  ADD KEY `p_id` (`p_id`);

--
-- Indexes for table `doctor`
--
ALTER TABLE `doctor`
  ADD PRIMARY KEY (`d_id`);

--
-- Indexes for table `patient`
--
ALTER TABLE `patient`
  ADD PRIMARY KEY (`p_id`);

--
-- Indexes for table `prescription`
--
ALTER TABLE `prescription`
  ADD PRIMARY KEY (`pres_id`),
  ADD KEY `p_id` (`p_id`),
  ADD KEY `d_id` (`d_id`);

--
-- Indexes for table `slot`
--
ALTER TABLE `slot`
  ADD PRIMARY KEY (`slot_id`);

--
-- Indexes for table `sos_alerts`
--
ALTER TABLE `sos_alerts`
  ADD PRIMARY KEY (`p_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `appointment`
--
ALTER TABLE `appointment`
  MODIFY `app_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `doctor`
--
ALTER TABLE `doctor`
  MODIFY `d_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `patient`
--
ALTER TABLE `patient`
  MODIFY `p_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `prescription`
--
ALTER TABLE `prescription`
  MODIFY `pres_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `slot`
--
ALTER TABLE `slot`
  MODIFY `slot_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointment`
--
ALTER TABLE `appointment`
  ADD CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`d_id`) REFERENCES `doctor` (`d_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `appointment_ibfk_2` FOREIGN KEY (`p_id`) REFERENCES `patient` (`p_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `prescription`
--
ALTER TABLE `prescription`
  ADD CONSTRAINT `prescription_ibfk_1` FOREIGN KEY (`d_id`) REFERENCES `doctor` (`d_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

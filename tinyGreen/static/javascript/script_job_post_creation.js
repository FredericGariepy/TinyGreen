//This Script disables and changes the schedule style and resets values depending on if it is checked or not
function toggleColumnClass(checkbox) {
    var columnIndex = checkbox.parentElement.parentElement.cellIndex; // Get column index
    var table = checkbox.closest('table');

    for (var i = 0; i < table.rows.length; i++) {
        var td = table.rows[i].cells[columnIndex];

        // Toggle the table-secondary class
        if (checkbox.checked) {
            td.classList.remove("table-secondary");
        } else {
            td.classList.add("table-secondary");
            // Clear the value of input elements inside the td
            var inputs = td.querySelectorAll("input[type='time']");
            inputs.forEach(function(input) {
                input.value = ""; // Reset the value
            });
        }

        // Disable/enable input elements inside the td
        var inputs = td.querySelectorAll("input[type='time']");
        inputs.forEach(function(input) {
            input.disabled = !checkbox.checked;
        });
    }
}
//this is a support script to make unchecked boxes return false
function isChecked(checkboxId) {
    var checkbox = document.getElementById(checkboxId);
    return checkbox ? checkbox.checked : false;
}

//this is a support function that gives the time in 12h format
function formatTime(time) {
    // catch empty strings
    if(time === ''){return false;}
    // Parse the time string
    var timeArray = time.split(':');
    var hours = parseInt(timeArray[0]);
    var minutes = parseInt(timeArray[1]);

    // Convert to 12-hour format
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // Handle midnight (0 hours)

    // Pad single digit hours and minutes with leading zeros
    hours = hours < 10 ? '0' + hours : hours;
    minutes = minutes < 10 ? '0' + minutes : minutes;

    // Return the formatted time string
    return hours + ':' + minutes + ' ' + ampm;
}

    // Function to set visibility for a specific day
function setDayVisibility(daySchedule, previewScheduleId, previewScheduleIdRow, previewScheduleIdStart, previewScheduleIdEnd, dayStartTime, dayEndTime) {
    if (daySchedule) {
        document.getElementById(previewScheduleId).style.display = 'inline-block';
        document.getElementById(previewScheduleIdRow).style.display = 'inline-block';
        document.getElementById(previewScheduleIdStart).textContent = dayStartTime;
        document.getElementById(previewScheduleIdEnd).textContent = dayEndTime;
    } else {
        document.getElementById(previewScheduleId).style.display = 'none';
        document.getElementById(previewScheduleIdRow).style.display = 'none';
    }
}

function setCustomScheduleVisibility(daySchdule,day,dayStart,dayEnd){
    if(daySchdule){
        document.getElementById(day+'-td-title').style.display = 'inline-block';
        document.getElementById(day+'-td-start').style.display = 'inline-block';
        document.getElementById(day+'-td-end').style.display = 'inline-block';
        document.getElementById(day+'-td-start').textContent = dayStart;
        document.getElementById(day+'-td-end').textContent = dayEnd;


    }else{
        document.getElementById(day+'-td-title').style.display = 'none';
        document.getElementById(day+'-td-start').style.display = 'none';
        document.getElementById(day+'-td-end').style.display = 'none';
    }
}
document.addEventListener('DOMContentLoaded', function(){
    
// this script sets up all the variables for the preview modal , js rendered client-side
document.getElementById('previewBtn').addEventListener('click', function() {
    
    // Necessary form data (optional = false)
    // BASIC INFORMATION
    var jobTitleElement = document.getElementById('job-title').value;
    var jobTitle = jobTitleElement ? jobTitleElement : 'missing title'; //check if not null

    var jobType = document.getElementById('job-type').value; //default: Full-time
    var jobLocation = document.getElementById('job-location').value; //default: Seoul

    var jobLocationDetailsElement = document.getElementById('job-details').value;
    var jobLocationDetails = jobLocationDetailsElement ? jobLocationDetailsElement : 'missing location details'; //check if not null
    
    var jobSalaryElement = document.getElementById('job-salary').value;
    var jobSalary = jobSalaryElement ? parseFloat(jobSalaryElement).toLocaleString('en-US') : 'missing salary'; //check if not null

    var jobPaymentType = document.getElementById('job-payment-type').value; //default: Monthly
    
    var jobNegotiable = isChecked('job-negotiable'); // default: false
    var jobNegotiableVisibility = jobNegotiable ? 'inline-block' : 'none'; 
    
    // job start date
    var jobStartDateElement = document.getElementById('job-startdate').value;
    var startDate = new Date(jobStartDateElement);
    var formattedDate = startDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    var jobStartDate = formattedDate !== 'Invalid Date' ? formattedDate: 'missing date'; 

    var jobAsapElement = isChecked('job-asap');
    var jobAsapVisibility = jobAsapElement ? 'inline-block' : 'none'; 
    var asapBadgeSPElement = document.getElementById('asap-badge-small-preview');
    asapBadgeSPElement.style.display = jobAsapVisibility;
    var asapBadgeBPElement = document.getElementById('asap-badge-big-preview');
    asapBadgeBPElement.style.display = jobAsapVisibility;
    
    // Optional form Data (optional = true) //default false
    // STUDENT TYPES
    var kindStudent = isChecked('kind_student');
    var kindStudentVisibility = kindStudent ? 'inline-block' : 'none'; 
    document.getElementById('preview-kind-student').style.display = kindStudentVisibility;
    
    var elemStudent = isChecked('elem_student');
    var elemStudentVisibility = elemStudent ? 'inline-block' : 'none'; 
    document.getElementById('preview-elem-student').style.display = elemStudentVisibility;

    var midlStudent = isChecked('midl_student');
    var midlStudentVisibility = midlStudent ? 'inline-block' : 'none'; 
    document.getElementById('preview-midl-student').style.display = midlStudentVisibility;

    var highStudent = isChecked('high_student');
    var highStudentVisibility = highStudent ? 'inline-block' : 'none'; 
    document.getElementById('preview-high-student').style.display = highStudentVisibility;

    var univStudent = isChecked('univ_student');
    var univStudentVisibility = univStudent ? 'inline-block' : 'none'; 
    document.getElementById('preview-univ-student').style.display = univStudentVisibility;

    var adltStudent = isChecked('adlt_student');
    var adltStudentVisibility = adltStudent ? 'inline-block' : 'none'; 
    document.getElementById('preview-adlt-student').style.display = adltStudentVisibility;

    //no student
    var noStudent = kindStudent || elemStudent || midlStudent || highStudent || univStudent || adltStudent;
    var noStudentVisbility =  noStudent ? 'none': 'inline-block' ;
    document.getElementById('preview-no-student').style.display = noStudentVisbility;


    // BENEFITS
    var healthInsurance = isChecked('health_insurance');
    var healthInsuranceVisibility = healthInsurance ? 'inline-block' : 'none'; 
    document.getElementById('preview-healthInsurance').style.display = healthInsuranceVisibility;

    var pension = isChecked('pension');
    var pensionVisibility = pension ? 'inline-block' : 'none'; 
    document.getElementById('preview-pension').style.display = pensionVisibility;

    var airfare = isChecked('airfare');
    var airfareVisibility = airfare ? 'inline-block' : 'none'; 
    document.getElementById('preview-airfare').style.display = airfareVisibility;

    var severance = isChecked('severance');
    var severanceVisibility = severance ? 'inline-block' : 'none'; 
    document.getElementById('preview-severance').style.display = severanceVisibility;

    var housing = isChecked('housing');
    var housingVisibility = housing ? 'inline-block' : 'none'; 
    document.getElementById('preview-housing').style.display = housingVisibility;

    var housingAllowanceFieldElement = document.getElementById("housingAllowanceField").value;
    var housingAllowanceField = housingAllowanceFieldElement !== '' ? parseFloat(housingAllowanceFieldElement).toLocaleString('en-US') : false;
    var housingAllowanceFieldVisibility = housingAllowanceField === false ? 'none': 'inline-block';
    document.getElementById('preview-housingAllowanceField').style.display = housingAllowanceFieldVisibility;
    document.getElementById('preview-housingAllowanceField-int').textContent = housingAllowanceField;

    var vacationDaysFieldElement = document.getElementById('vacationDaysField').value;
    var vacationDaysField = vacationDaysFieldElement !=='' ? vacationDaysFieldElement : false;
    var vacationDaysFieldVisibility = vacationDaysField === false ? 'none': 'inline-block';
    document.getElementById('preview-vacationDaysField').style.display = vacationDaysFieldVisibility;
    document.getElementById('preview-vacationDaysField-int').textContent =vacationDaysField;

    var benefitsPresent = healthInsurance || pension || airfare || severance || housing || housingAllowanceField || vacationDaysField ;
    var benefitsPresentVisiblity = benefitsPresent === false ? 'none': 'inline-block';
    document.getElementById('benefitsPresentVisiblity').style.display = benefitsPresentVisiblity;

    
    // job Description
    var jobDescriptionElement = document.getElementById('job-description').value;
    var jobDescription = jobDescriptionElement ? jobDescriptionElement : 'Missing a job description';
    // Update modal description
    document.getElementById('preview-description').textContent = jobDescription;
    
    
    // Update modal content for Necessary form data (optional = false)
    // MODAL STYLING OF NECCESARY DATA
    document.getElementById('preview-title').textContent = jobTitle;
    document.getElementById('preview-title-big').textContent = jobTitle;
    
    if (jobTitle === 'missing title') {
        document.getElementById('preview-title').classList.add('text-danger'); // Add the 'text-danger' class
        document.getElementById('preview-title-big').classList.add('text-danger'); // Add the 'text-danger' class
    }else{
        document.getElementById('preview-title').classList.remove('text-danger'); // Add the 'text-danger' class
        document.getElementById('preview-title-big').classList.remove('text-danger'); // Add the 'text-danger' class
    }
    
    document.getElementById('preview-type').textContent = jobType;
    document.getElementById('preview-type-big').textContent = jobType;

    document.getElementById('preview-location').textContent = jobLocation;
    document.getElementById('preview-location-big').textContent = jobLocation;

    document.getElementById('preview-location-details').textContent = jobLocationDetails;
    if (jobLocationDetails === 'missing location details') {
        document.getElementById('preview-location-details').classList.add('text-danger'); // Add the 'text-danger' class
    }else{
        document.getElementById('preview-location-details').classList.remove('text-danger'); // Add the 'text-danger' class
    }
    
    document.getElementById('preview-salary').textContent = jobSalary;
    document.getElementById('preview-salary-big').textContent = jobSalary;
    if (jobSalary === 'missing salary') {
        document.getElementById('preview-salary').classList.add('text-danger'); // Add the 'text-danger' class
        document.getElementById('preview-salary-big').classList.add('text-danger'); // Add the 'text-danger' class
    }else{
        document.getElementById('preview-salary').classList.remove('text-danger'); // Add the 'text-danger' class
        document.getElementById('preview-salary-big').classList.remove('text-danger'); // Add the 'text-danger' class
    }
    
    document.getElementById('preview-payment-type').textContent = jobPaymentType;
    document.getElementById('preview-payment-type-big').textContent = jobPaymentType;
    
    var jobNegotiableElment = document.getElementById('preview-negotiable');
    jobNegotiableElment.style.display = jobNegotiableVisibility;
    
    // job start Date
    if (jobStartDate !== 'missing date') {
        var date = new Date(jobStartDate); // Parse the date string
        var options = { month: 'short', day: '2-digit' }; // Define options for formatting
        var jobStartDate_formattedDate = date.toLocaleDateString('en-US', options); // Format the date
        document.getElementById('preview-startdate').textContent = jobStartDate_formattedDate; // Update the element
        document.getElementById('preview-startdate').classList.remove('text-danger'); // Add the 'text-danger' class
        
        document.getElementById('preview-startdate-big').textContent = jobStartDate_formattedDate; // Update the element
        document.getElementById('preview-startdate-big').classList.remove('text-danger'); // Add the 'text-danger' class
    } else {
        document.getElementById('preview-startdate').textContent = jobStartDate; // Update the element with 'missing'
        document.getElementById('preview-startdate').classList.add('text-danger'); // Add the 'text-danger' class
        
        document.getElementById('preview-startdate-big').textContent = jobStartDate; // Update the element with 'missing'
        document.getElementById('preview-startdate-big').classList.add('text-danger'); // Add the 'text-danger' class
    }
    
    // WORK SCHEDULES 

    // default schedule (monday to friday)
    var everydayStartTimeElement = document.getElementById('everyday_start_time').value;
    var everydayStartTime = formatTime(everydayStartTimeElement);
    
    var everydayEndTimeElement = document.getElementById('everyday_end_time').value;
    var everydayEndTime = formatTime(everydayEndTimeElement);
    
    // IF default schedule being used
    // update modals visbility
    var defaultSchedule = everydayStartTime !== false && everydayEndTime !== false;
    var defaultScheduleVisibility = defaultSchedule ? 'inline-block' : 'none';
    document.getElementById('preview-default-schedule').style.display = defaultScheduleVisibility;
    document.getElementById('preview-default-schedule-visibility').style.display = defaultScheduleVisibility;

    document.getElementById('preview-everyday_start_time').textContent = everydayStartTime;
    document.getElementById('preview-everyday_start_time-td').textContent = everydayStartTime;
    document.getElementById('preview-everyday_end_time').textContent = everydayEndTime;
    document.getElementById('preview-everyday_end_time-td').textContent = everydayEndTime;
    
    
    // Custom (start times)
    // setting variables with data from FORM
    var mondayStartTimeElement = document.getElementById('monday_start_time').value;
    var mondayStartTime = formatTime(mondayStartTimeElement);
    
    var tuesdayStartTimeElement = document.getElementById('tuesday_start_time').value;
    var tuesdayStartTime = formatTime(tuesdayStartTimeElement);
    
    var wednesdayStartTimeElement = document.getElementById('wednesday_start_time').value;
    var wednesdayStartTime = formatTime(wednesdayStartTimeElement);
    
    var thursdayStartTimeElement = document.getElementById('thursday_start_time').value;
    var thursdayStartTime = formatTime(thursdayStartTimeElement);
    
    var fridayStartTimeElement = document.getElementById('friday_start_time').value;
    var fridayStartTime = formatTime(fridayStartTimeElement);
    
    var saturdayStartTimeElement = document.getElementById('saturday_start_time').value;
    var saturdayStartTime = formatTime(saturdayStartTimeElement);
    
    var sundayStartTimeElement = document.getElementById('sunday_start_time').value;
    var sundayStartTime = formatTime(sundayStartTimeElement);
    
    // Custom (end times)
    var mondayEndTimeElement = document.getElementById('monday_end_time').value;
    var mondayEndTime = formatTime(mondayEndTimeElement);
    
    var tuesdayEndTimeElement = document.getElementById('tuesday_end_time').value;
    var tuesdayEndTime = formatTime(tuesdayEndTimeElement);
    
    var wednesdayEndTimeElement = document.getElementById('wednesday_end_time').value;
    var wednesdayEndTime = formatTime(wednesdayEndTimeElement);
    
    var thursdayEndTimeElement = document.getElementById('thursday_end_time').value;
    var thursdayEndTime = formatTime(thursdayEndTimeElement);
    
    var fridayEndTimeElement = document.getElementById('friday_end_time').value;
    var fridayEndTime = formatTime(fridayEndTimeElement);
    
    var saturdayEndTimeElement = document.getElementById('saturday_end_time').value;
    var saturdayEndTime = formatTime(saturdayEndTimeElement);
    
    var sundayEndTimeElement = document.getElementById('sunday_end_time').value;
    var sundayEndTime = formatTime(sundayEndTimeElement);
    
    // Custom Day schedules 
    // Check if a day is active (has both START && END)
    var mondaySchedule= mondayStartTime !== false && mondayEndTime !== false;
    var tuesdaySchedule= tuesdayStartTime !== false && tuesdayEndTime !== false;
    var wednesdaySchedule= wednesdayStartTime !== false && wednesdayEndTime !== false;
    var thursdaySchedule= thursdayStartTime !== false && thursdayEndTime !== false;
    var fridaySchedule= fridayStartTime !== false && fridayEndTime !== false;
    var saturdaySchedule= saturdayStartTime !== false && saturdayEndTime !== false;
    var sundaySchedule= sundayStartTime !== false && sundayEndTime !== false;


    // Set Day schedulde VISIBILITY
    setDayVisibility(mondaySchedule,'preview-monday-schedule','preview-monday-schedule-row','preview-monday-start-time','preview-monday-end-time',mondayStartTime,mondayEndTime);
    setDayVisibility(tuesdaySchedule, 'preview-tuesday-schedule', 'preview-tuesday-schedule-row', 'preview-tuesday-start-time', 'preview-tuesday-end-time', tuesdayStartTime, tuesdayEndTime);
    setDayVisibility(wednesdaySchedule, 'preview-wednesday-schedule', 'preview-wednesday-schedule-row', 'preview-wednesday-start-time', 'preview-wednesday-end-time', wednesdayStartTime, wednesdayEndTime);
    setDayVisibility(thursdaySchedule, 'preview-thursday-schedule', 'preview-thursday-schedule-row', 'preview-thursday-start-time', 'preview-thursday-end-time', thursdayStartTime, thursdayEndTime);
    setDayVisibility(fridaySchedule, 'preview-friday-schedule', 'preview-friday-schedule-row', 'preview-friday-start-time', 'preview-friday-end-time', fridayStartTime, fridayEndTime);
    setDayVisibility(saturdaySchedule, 'preview-saturday-schedule', 'preview-saturday-schedule-row', 'preview-saturday-start-time', 'preview-saturday-end-time', saturdayStartTime, saturdayEndTime);
    setDayVisibility(sundaySchedule, 'preview-sunday-schedule', 'preview-sunday-schedule-row', 'preview-sunday-start-time', 'preview-sunday-end-time', sundayStartTime, sundayEndTime);
    
    setCustomScheduleVisibility(mondaySchedule,'monday',mondayStartTime,mondayEndTime);
    setCustomScheduleVisibility(tuesdaySchedule, 'tuesday', tuesdayStartTime, tuesdayEndTime);
    setCustomScheduleVisibility(wednesdaySchedule, 'wednesday', wednesdayStartTime, wednesdayEndTime);
    setCustomScheduleVisibility(thursdaySchedule, 'thursday', thursdayStartTime, thursdayEndTime);
    setCustomScheduleVisibility(fridaySchedule, 'friday', fridayStartTime, fridayEndTime);
    setCustomScheduleVisibility(saturdaySchedule, 'saturday', saturdayStartTime, saturdayEndTime);
    setCustomScheduleVisibility(sundaySchedule, 'sunday', sundayStartTime, sundayEndTime);

    // IF custom schedule being used
    // update modals visbility
    var customSchedulePresent = mondaySchedule||tuesdaySchedule||wednesdaySchedule||thursdaySchedule||fridaySchedule||saturdaySchedule||sundaySchedule;
    var customSchedulePresentVisibility = customSchedulePresent ? 'inline-block' : 'none';
    document.getElementById('preview-custom-schedule-visibility').style.display = customSchedulePresentVisibility;
    
    // unspecified schedule
    var unspecifiedSchedule = defaultSchedule || customSchedulePresent;
    console.log(unspecifiedSchedule);
    var unspecifiedScheduleVisibility = unspecifiedSchedule? 'none': 'inline-block';
    document.getElementById('preview-unspecified-schedule').style.display = unspecifiedScheduleVisibility;
    document.getElementById('preview-unspecified-schedule-div').style.display = unspecifiedScheduleVisibility;
});
});

function resetForm() {
    // Reset values for everyday start and end time
    document.getElementById('everyday_start_time').value = '';
    document.getElementById('everyday_end_time').value = '';

    // Reset values for custom working days
    var days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];

    for (var i = 0; i < days.length; i++) {
        var day = days[i];

        // Reset start time
        document.getElementById(day + '_start_time').value = '';

        // Reset end time
        document.getElementById(day + '_end_time').value = '';

        // Reset checkbox to checked
        var checkbox = document.getElementById('flexCheck' + day);
        checkbox.checked = true;

        // Remove "table-secondary" class
        var columnIndex = checkbox.parentElement.parentElement.cellIndex;
        var table = checkbox.closest('table');

        for (var j = 0; j < table.rows.length; j++) {
            var td = table.rows[j].cells[columnIndex];
            td.classList.remove("table-secondary");
        }

        // Enable the start input
        var inputStartElement = document.getElementById(day + '_start_time');
        inputStartElement.removeAttribute("disabled");

        // Enable the end input
        var inputEndElement = document.getElementById(day + '_end_time');
        inputEndElement.removeAttribute("disabled");
    }
}

document.addEventListener("DOMContentLoaded", function () {
    var housingCheckbox = document.getElementById("housingCheckbox");
    var housingAllowanceField = document.getElementById("housingAllowanceField");

    housingCheckbox.addEventListener("change", function () {
        // Enable or disable the housing allowance field based on the checkbox state
        housingAllowanceField.disabled = !housingCheckbox.checked;
    });
});


document.addEventListener("DOMContentLoaded", function () {
    // Get references to the checkbox and the vacation days field
    var vacationCheckbox = document.getElementById("vacationCheckbox");
    var vacationDaysField = document.getElementById("vacationDaysField");

    // Add an event listener to the checkbox
    vacationCheckbox.addEventListener("change", function () {
        // Enable or disable the vacation days field based on the checkbox state
        vacationDaysField.disabled = !vacationCheckbox.checked;
    });
});

function updateCharacterCount(textarea) {
    var maxLength = 1000;
    var currentLength = textarea.value.length;
    var remainingCharacters = maxLength - currentLength;
    var characterCountElement = document.getElementById('characterCount');
    characterCountElement.textContent = remainingCharacters + ' characters remaining';
}

// Initialize character count on page load
document.addEventListener("DOMContentLoaded", function () {
    var textarea = document.querySelector('[name="description"]');
    if (textarea) {
        updateCharacterCount(textarea);
    }
});

// This Jquery limits front end input digits
$(document).ready(function () {
    $('#job-salary, #vacationDaysField, #housingAllowanceField').on('input', function () {
        var maxLength;
        switch ($(this).attr('id')) {
            case 'job-salary':
                maxLength = 8;
                break;
            case 'vacationDaysField':
                maxLength = 3;
                break;
            case 'housingAllowanceField':
                maxLength = 7;
                break;
        }
        var value = $(this).val();
        if (value.length > maxLength) {
            $(this).val(value.slice(0, maxLength));
        }
    });
});

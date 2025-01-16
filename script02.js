const basePath = "plots/"; // Base folder path for images
document.addEventListener('DOMContentLoaded', () => {
    const fileDropdown = document.getElementById('file-dropdown');
    const tabDropdown = document.getElementById('tab-dropdown');
    const partnerDropdown = document.getElementById('partner-dropdown');
    const partnerImage = document.getElementById('partner-image');
    const partnerImageSrc = document.getElementById('partner-image-src');

    // Load the data from the JSON file
    fetch('files_data.json')
        .then(response => response.json())
        .then(filesData => {
            // Populate File Dropdown
            Object.keys(filesData).forEach(file => {
                const option = document.createElement('option');
                option.value = file;
                option.textContent = file;
                fileDropdown.appendChild(option);
            });

            // Handle File Dropdown change
            fileDropdown.addEventListener('change', () => {
                const selectedFile = fileDropdown.value;

                // Reset and disable Tab and Partner dropdowns
                tabDropdown.innerHTML = '<option value="">--Select Tab--</option>';
                partnerDropdown.innerHTML = '<option value="">--Select Partner--</option>';
                partnerDropdown.disabled = true;
                tabDropdown.disabled = !selectedFile;

                if (selectedFile) {
                    // Populate Tab Dropdown
                    Object.keys(filesData[selectedFile]).forEach(tab => {
                        const option = document.createElement('option');
                        option.value = tab;
                        option.textContent = tab;
                        tabDropdown.appendChild(option);
                    });
                }
            });

            // Handle Tab Dropdown change
            tabDropdown.addEventListener('change', () => {
                const selectedFile = fileDropdown.value;
                const selectedTab = tabDropdown.value;

                // Reset Partner dropdown
                partnerDropdown.innerHTML = '<option value="">--Select Partner--</option>';
                partnerDropdown.disabled = !selectedTab;

                if (selectedTab) {
                    // Populate Partner Dropdown
                    filesData[selectedFile][selectedTab].forEach(partner => {
                        const option = document.createElement('option');
                        option.value = partner;
                        option.textContent = partner;
                        partnerDropdown.appendChild(option);
                    });
                }
            });

            // Handle Partner Dropdown change (for image display)
            partnerDropdown.addEventListener('change', () => {
                const selectedFile = fileDropdown.value;
                const selectedTab = tabDropdown.value;
                const selectedPartner = partnerDropdown.value;

                if (selectedFile && selectedTab && selectedPartner) {
                    const imagePath = `${basePath}/${selectedFile}/${selectedTab}/${selectedPartner}/${selectedPartner}.jpg`;
                    partnerImageSrc.src = imagePath;
                    partnerImage.style.display = 'block';
                } else {
                    partnerImage.style.display = 'none';
                }
            });
        });
});

function show_cctv(event) {
    event.preventDefault();
    main_body = document.getElementById("main_body");
    form_input = document.getElementById("input_form");
    password = form_input.elements[0].value;
    button = form_input.elements[1];
    button.disabled = true;
    form_input.elements[0].value = null;
    fetch(`/cctv?p=${encodeURIComponent(password)}`)
        .then(response => {
            if (response.status === 200) {
                cctv_img = document.createElement("img");
                cctv_img.src = `/cctv?p=${encodeURIComponent(password)}`;
                main_body.append(cctv_img);
                form_input.style.display = "none";
            } else if (response.status === 401) {
                alert("Unauthorized: Invalid password");
                button.disabled = false;
            } else {
                alert("Error: " + response.status);
                button.disabled = false;
            }
        })
        .catch(error => {
            console.error("Error fetching CCTV stream:", error);
            alert("Error connecting to the server.");
            button.disabled = false;
        });
}
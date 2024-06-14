function renderSourceView(calendarResponse) {

    // Clean out existing content
    launchCalendarCard = document.getElementById("launchCalendarCardBody");
    launchCalendarCard.innerHTML = '';

    sourcesList = document.createElement('ul');
    sourcesList.classList.add("list-group", "list-group-flush", 'pt-3')

    // Scrape details row
    li=document.createElement('li');
    li.classList.add("list-group-item");

    // Scrape details
    lastUpdated = document.createElement('p');
    lastUpdated.classList.add("text-muted", "pt-1", "pb-1");
    lastUpdated.innerHTML = calendarResponse.calendar.length + " unique launches from " + calendarResponse.sources.length + " different sources. " + "Read at " + calendarResponse.last_updated + ". The sources below did all the hard work to get this information, I merely aggregated it.";
    li.appendChild(lastUpdated);
    sourcesList.appendChild(li);

    if (calendarResponse.sources.length > 0) {
        for (const source of calendarResponse.sources) {
            // list item
            li=document.createElement('li');
            li.classList.add("list-group-item", "d-flex", "justify-content-between", "align-items-start");

            // link
            a = document.createElement('a');
            textColour = "text-" + SourceColourMap[source.name];
            a.classList.add(textColour, "me-auto", "p-1");
            a.innerHTML = source.name;
            a.href = source.url;
            li.appendChild(a);

            // launch count
            span = document.createElement('span');
            span.id = 'launchCounter';
            span.classList.add("badge", "rounded-pill", "m-1", "bg-" + SourceColourMap[source.name]);
            span.innerHTML = source.count;
            li.appendChild(span);

            sourcesList.appendChild(li)
        }
    }

    // Scrape button row
    li=document.createElement('li');
    li.classList.add("list-group-item", 'p-3', 'd-flex', 'justify-content-center');

    // Button
    scrapeButton = document.createElement('button');
    scrapeButton.id="scrapeButton";
    scrapeButton.type="button";
    scrapeButton.classList.add("btn", "btn-outline-dark", "m-1");
    scrapeButton.innerHTML = "<strong>Refresh</strong>";
    scrapeButton.onclick = scrapeButtonHandler;
    li.appendChild(scrapeButton);

    sourcesList.appendChild(li);
    launchCalendarCard.appendChild(sourcesList)


    // Spinner
    spinner = document.createElement('div');
    spinner.id = "scrappingSpinner";
    spinner.style.display = 'none';
    spinner.classList.add("spinner-border", "text-dark");
    spinner.role = "status";
    spinnerSpan = document.createElement('span');
    spinnerSpan.classList.add("sr-only", 'p-1');

    spinner.appendChild(spinnerSpan);
    li.appendChild(spinner);
}

window.addEventListener('load', function() {
    getJSONCallback("http://192.168.0.48:8080/api/calendar", renderSourceView)
})

function renderLaunchCalendar(calendarResponse) {
    // Clean out existing content
    launchCalendarCard = document.getElementById("launchCalendarCardBody");
    launchCalendarCard.innerHTML = '';

    // Search bar
    form = document.createElement('form');
    form.classList.add("d-flex", "p-3", 'pt-4');
    input = document.createElement('input');
    input.classList.add("form-control");
    input.id = "searchTextField";
    input.type = "search";
    input.placeholder="Search launches";
    input.onchange = searchButtonHandler;
    form.appendChild(input);
    launchCalendarCard.appendChild(form);

    // Calendar
    calendarList = document.createElement('ul');
    calendarList.classList.add("list-group", "list-group-flush")
    if (calendarResponse.calendar.length > 0) {
        for (const launch of calendarResponse.calendar) {
            // list item
            li=document.createElement('li');
            li.classList.add("list-group-item");

            // title
            titleElement = document.createElement('h3');
            titleElement.classList.add("display-7");
            titleElement.innerHTML = launch.name
            li.appendChild(titleElement);

            // T-0
            tZeroElement = document.createElement('h6');
            tZeroElement.classList.add("mb-2", "text-muted");
            tZeroElement.innerHTML = launch.t_zero
            li.appendChild(tZeroElement);

            // sources
            for (const i in launch.sources) {
                source = launch.sources[i];
                sourceElement = document.createElement('a');
                sourceElement.href = '/sources?n=' + source.name
                sourceElement.innerHTML = source.name;
                sourceElement.classList.add("text-" + SourceColourMap[source.name]);
                li.appendChild(sourceElement);

                if (i < launch.sources.length - 1) {
                    seperatorElement = document.createElement('span');
                    seperatorElement.classList.add("text-muted");
                    seperatorElement.innerHTML = " | "
                    li.appendChild(seperatorElement);
                }
            }
            calendarList.appendChild(li);
        }
    } else {
        console.log('None found!');
        li=document.createElement('li');
        li.classList.add("list-group-item");
        p=document.createElement('p');
        p.classList.add("text-muted", "text-center");
        p.innerHTML = "No launches found :(";
        li.appendChild(p);
        calendarList.appendChild(li);
    }
    launchCalendarCard.appendChild(calendarList);

}

function filterLaunchCalendar(calendarResponse) {
    searchString = document.getElementById("searchTextField").value;
    if (searchString != "") {
        filteredLaunches = [];
        for (const launch of calendarResponse.calendar) {
            if (launch.name.toLowerCase().includes(searchString.toLowerCase())) {
                filteredLaunches.push(launch);
            }
        }
    calendarResponse.calendar = filteredLaunches;
    }
    renderLaunchCalendar(calendarResponse);
}


function searchButtonHandler() {
    clone = { ...cachedCalendarResponse }
    filterLaunchCalendar(clone);
}

function renderInitialLaunchCalendar(launchCalendar) {
    cachedCalendarResponse = launchCalendar;
    renderLaunchCalendar(launchCalendar);
}

window.addEventListener('load', function() {
    getJSONCallback("http://192.168.0.48:8080/api/calendar", renderInitialLaunchCalendar)
})
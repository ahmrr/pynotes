const home = document.getElementById("home");
const homeOl = home.children[2];
const pages = [home];

const router = new Navigo("/");

router.on("/docs/index.html", () => {
    for (const page of pages) page.classList.remove("current");

    home.classList.add("current");

    console.log("Navigated to home using Navigo");
});

console.log(Object.entries(config.classes));

for (const [semester, courses] of Object.entries(config.classes)) {
    const page = document.body.appendChild(document.createElement("main"));
    page.id = semester.toLowerCase().replaceAll(" ", "");
    page.classList.add("page");
    pages.push(page);

    const header = page.appendChild(document.createElement("h1"));
    header.textContent = semester;
    page.appendChild(document.createElement("hr"));

    const anchor = homeOl
        .appendChild(document.createElement("li"))
        .appendChild(document.createElement("a"));
    anchor.href = `/${page.id}`;
    anchor.textContent = semester;
    anchor.addEventListener("click", (event) => {
        event.preventDefault();
        router.navigate(`/${page.id}`);
    });

    router.on(`/${page.id}`, () => {
        for (const page of pages) page.classList.remove("current");

        page.classList.add("current");

        console.log(`Navigated to ${semester} using Navigo`);
    });

    const semesterOl = page.appendChild(document.createElement("ol"));

    for (const course of courses) {
        const coursePage = document.body.appendChild(
            document.createElement("main")
        );
        coursePage.id = course.toLowerCase().replaceAll(" ", "");
        coursePage.classList.add("page");
        pages.push(coursePage);

        const courseHeader = coursePage.appendChild(
            document.createElement("h1")
        );
        courseHeader.textContent = course;
        coursePage.appendChild(document.createElement("hr"));

        const courseAnchor = semesterOl
            .appendChild(document.createElement("li"))
            .appendChild(document.createElement("a"));
        courseAnchor.href = `/${page.id}/${coursePage.id}`;
        courseAnchor.textContent = course;
        courseAnchor.addEventListener("click", (event) => {
            event.preventDefault();
            router.navigate(`/${page.id}/${coursePage.id}`);
        });

        router.on(`/${page.id}/${coursePage.id}`, () => {
            for (const page of pages) page.classList.remove("current");

            coursePage.classList.add("current");

            console.log(`Navigated to ${semester}/${course} using Navigo`);
        });

        const courseOl = coursePage.appendChild(document.createElement("ol"));

        console.log(data.files);

        for (const file of data.files) {
            console.log(file.split("/")[2] + " | " + course);
            console.log(file.split("/")[2] === course);
            if (file.split("/")[2] === course) {
                console.log("note added");
                const fileAnchor = courseOl
                    .appendChild(document.createElement("li"))
                    .appendChild(document.createElement("a"));
                fileAnchor.href = "/" + file;
                fileAnchor.textContent = file.split("/")[3].split(".")[0];
            }
        }
    }
}

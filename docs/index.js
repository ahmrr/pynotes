const home = document.getElementById("home");
const pages = [home];

const router = new Navigo("/");

console.log(Object.entries(config.classes));

for (const [semester, classes] of Object.entries(config.classes)) {
    const page = document.body.appendChild(document.createElement("main"));
    pages.push(page);

    page.id = semester.toLowerCase().replaceAll(" ", "");

    const anchor = home.appendChild(document.createElement("a"));

    anchor.textContent = semester;
    anchor.href = `/${page.id}`;

    router.on(`/${page.id}`, () => {
        page.classList.add("active");

        for (const page of pages)
            if (page.id !== page.id) page.classList.remove("active");

        console.log(`Navigated to ${semester}`);
    });

    for (const course of classes) {
        router.on(
            `/${page.id}/${course.toLowerCase().replaceAll(" ", "")}`,
            () => {
                console.log(`Navigated to ${semester}/${course}`);
            }
        );
    }
}

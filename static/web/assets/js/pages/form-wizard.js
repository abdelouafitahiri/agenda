const step1Next = document.getElementById("step1Next"),
    step1Tab = document.getElementById("step1-tab"),
    step1 = document.getElementById("step1"),
    step2Next = document.getElementById("step2Next"),
    step2Prev = document.getElementById("step2Prev"),
    step2Tab = document.getElementById("step2-tab"),
    step2 = document.getElementById("step2"),
    step3Next = document.getElementById("step3Next"),
    step3Prev = document.getElementById("step3Prev"),
    step3Tab = document.getElementById("step3-tab"),
    step3 = document.getElementById("step3"),
    step4Next = document.getElementById("step4Next"),
    step4Prev = document.getElementById("step4Prev"),
    step4Tab = document.getElementById("step4-tab"),
    step4 = document.getElementById("step4"),
    step5Next = document.getElementById("step5Next"),
    step5Prev = document.getElementById("step5Prev"),
    step5Tab = document.getElementById("step5-tab"),
    step5 = document.getElementById("step5"),
    step6Prev = document.getElementById("step6Prev"),
    step6Tab = document.getElementById("step6-tab"),
    step6 = document.getElementById("step6"),
    step7Prev = document.getElementById("step7Prev"),
    step7Tab = document.getElementById("step7-tab"),
    step7 = document.getElementById("step7");


// Passer de l'étape 1 à l'étape 2
step1Next.addEventListener("click", function () {
    step1Tab.classList.remove("active"); // Désactiver l'onglet de l'étape 1
    step1.classList.remove("active", "show"); // Masquer le contenu de l'étape 1
    step2Tab.classList.add("active"); // Activer l'onglet de l'étape 2
    step2.classList.add("active", "show"); // Afficher le contenu de l'étape 2
});

// Revenir de l'étape 2 à l'étape 1
step2Prev.addEventListener("click", function () {
    step2Tab.classList.remove("active"); // Désactiver l'onglet de l'étape 2
    step2.classList.remove("active", "show"); // Masquer le contenu de l'étape 2
    step1Tab.classList.add("active"); // Activer l'onglet de l'étape 1
    step1.classList.add("active", "show"); // Afficher le contenu de l'étape 1
});

// Passer de l'étape 2 à l'étape 3
step2Next.addEventListener("click", function () {
    step2Tab.classList.remove("active"); // Désactiver l'onglet de l'étape 2
    step2.classList.remove("active", "show"); // Masquer le contenu de l'étape 2
    step3Tab.classList.add("active"); // Activer l'onglet de l'étape 3
    step3.classList.add("active", "show"); // Afficher le contenu de l'étape 3
});

// Revenir de l'étape 3 à l'étape 2
step3Prev.addEventListener("click", function () {
    step3Tab.classList.remove("active"); // Désactiver l'onglet de l'étape 3
    step3.classList.remove("active", "show"); // Masquer le contenu de l'étape 3
    step2Tab.classList.add("active"); // Activer l'onglet de l'étape 2
    step2.classList.add("active", "show"); // Afficher le contenu de l'étape 2
});

// Passer de l'étape 3 à l'étape 4
step3Next.addEventListener("click", function () {
    step3Tab.classList.remove("active"); // Désactiver l'onglet de l'étape 3
    step3.classList.remove("active", "show"); // Masquer le contenu de l'étape 3
    step4Tab.classList.add("active"); // Activer l'onglet de l'étape 4
    step4.classList.add("active", "show"); // Afficher le contenu de l'étape 4
});

// Revenir de l'étape 4 à l'étape 3
step4Prev.addEventListener("click", function () {
    step4Tab.classList.remove("active"); // Désactiver l'onglet de l'étape 4
    step4.classList.remove("active", "show"); // Masquer le contenu de l'étape 4
    step3Tab.classList.add("active"); // Activer l'onglet de l'étape 3
    step3.classList.add("active", "show"); // Afficher le contenu de l'étape 3
});
// Passer de l'étape 4 à l'étape 5
step4Next.addEventListener("click", function () {
    step4Tab.classList.remove("active");
    step4.classList.remove("active", "show");
    step5Tab.classList.add("active");
    step5.classList.add("active", "show");
});

// Revenir de l'étape 5 à l'étape 4
step5Prev.addEventListener("click", function () {
    step5Tab.classList.remove("active");
    step5.classList.remove("active", "show");
    step4Tab.classList.add("active");
    step4.classList.add("active", "show");
});

// Passer de l'étape 5 à l'étape 6
step5Next.addEventListener("click", function () {
    step5Tab.classList.remove("active");
    step5.classList.remove("active", "show");
    step6Tab.classList.add("active");
    step6.classList.add("active", "show");
});

// Revenir de l'étape 6 à l'étape 5
step6Prev.addEventListener("click", function () {
    step6Tab.classList.remove("active");
    step6.classList.remove("active", "show");
    step5Tab.classList.add("active");
    step5.classList.add("active", "show");
});

// Passer de l'étape 6 à l'étape 7
step6Next.addEventListener("click", function () {
    step6Tab.classList.remove("active");
    step6.classList.remove("active", "show");
    step7Tab.classList.add("active");
    step7.classList.add("active", "show");
});

// Revenir de l'étape 7 à l'étape 6
step7Prev.addEventListener("click", function () {
    step7Tab.classList.remove("active");
    step7.classList.remove("active", "show");
    step6Tab.classList.add("active");
    step6.classList.add("active", "show");
});

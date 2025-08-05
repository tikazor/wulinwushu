(function waitForJquery(){
    if (typeof window.django !== "undefined" && typeof window.django.jQuery !== "undefined") {
        var $ = window.django.jQuery;

        function normalizeString(str) {
            return str ? str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase() : "";
        }

        $(document).ready(function() {
            $('.selector-available input[type="text"]').each(function() {
                var $searchBox = $(this);
                var $selector = $searchBox.closest('.selector');
                var $selectBox = $selector.find('.selector-available select');
                var $chosenBox = $selector.find('.selector-chosen select');

                // On retire tous les anciens handlers (notamment Django natif !)
                $searchBox.off();
                console.log("Recherche native retirée, patch accent-insensitive appliqué !");


                // Sauvegarde la liste complète d'origine une fois pour toutes
                var allOptions = $selectBox.find('option').map(function() {
                    return {
                        value: this.value,
                        text: $(this).text()
                    };
                }).get();

                $searchBox.on('input.accentInsensitive', function() {
                    var search = normalizeString($(this).val());
                    var chosenValues = $chosenBox.find('option').map(function() { return this.value; }).get();
                    $selectBox.empty();
                    allOptions.forEach(function(opt) {
                        if (chosenValues.indexOf(opt.value) === -1 &&
                            normalizeString(opt.text).indexOf(search) !== -1) {
                            $selectBox.append($('<option>').val(opt.value).text(opt.text));
                        }
                    });
                });

                // Réinitialise si on efface le champ
                $searchBox.on('change.accentInsensitive', function() {
                    if (!$(this).val()) {
                        var chosenValues = $chosenBox.find('option').map(function() { return this.value; }).get();
                        $selectBox.empty();
                        allOptions.forEach(function(opt) {
                            if (chosenValues.indexOf(opt.value) === -1) {
                                $selectBox.append($('<option>').val(opt.value).text(opt.text));
                            }
                        });
                    }
                });
            });
        });
    } else {
        setTimeout(waitForJquery, 50);
    }
})();

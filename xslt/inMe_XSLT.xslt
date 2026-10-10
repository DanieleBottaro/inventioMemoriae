<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
    
    <xsl:template match="/">
        <html>
            <head>
                <title><xsl:value-of select="//tei:titleStmt/tei:title[@type='main']"/></title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous"></link>

                <link href="../style/xsl_style.css" rel="stylesheet"/>
            </head>
            <body class="py-5 min-vh-100">
                
                
                <div class="container-fluid mb-5">
                    <header class="row w-100 m-0 mb-5 text-center">
                        <div class="col-12">
                            <h1 class="text-purple-title"><xsl:value-of select="//tei:titleStmt/tei:title[@type='main']"/></h1>
                            <h2 class="text-light fs-4"><xsl:value-of select="//tei:titleStmt/tei:title[@type='sub']"/></h2>
                        </div>
                    </header>
                    
                    <hr/>

                    
                    <div class="row w-100">
                        <div class="container">
                            <h2 class="text-purple-title text-center mb-5">SOURCES</h2>
                        </div>
                    </div>
                    

                    <div class="row w-100 m-0">
                        <xsl:apply-templates select="//tei:listBibl[@type='sources']" />
                    </div>

                    <div class="row w-100">
                        <div class="container">
                            <h2 class="text-purple-title text-center  mt-5">SNIPPETS</h2>
                        </div>  
                    </div>  

                    <div class="container mt-5">
                        <xsl:apply-templates select="//tei:div[@type='excerpts']" />
                    </div>
                    
                    <div class="row w-100">
                        <div class="container">
                            <h2 class="text-purple-title text-center mb-5">ENTITIES EXTRACTED</h2>
                        </div>
                    </div>  

                    <!-- ==========  MENU DELLE TAB  ============== -->
                    <ul class="nav nav-underline justify-content-center mb-5" id="entityTabs" role="tablist">
                        <li class="nav-item" role="presentation">
                            <!-- NOTA: data-bs-target punta all'ID del contenuto da mostrare (es. #personaggi-pane) -->
                            <button class="nav-link custom-tab active" id="people-tab" data-bs-toggle="tab" data-bs-target="#people-pane" type="button" role="tab">People</button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link custom-tab" id="places-tab" data-bs-toggle="tab" data-bs-target="#places-pane" type="button" role="tab">Places</button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link custom-tab" id="events-tab" data-bs-toggle="tab" data-bs-target="#events-pane" type="button" role="tab">Events</button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link custom-tab" id="organizations-tab" data-bs-toggle="tab" data-bs-target="#organizations-pane" type="button" role="tab">Organizations</button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link custom-tab" id="artworks-tab" data-bs-toggle="tab" data-bs-target="#artworks-pane" type="button" role="tab">Artworks</button>
                        </li>
                    </ul> 

                    <!-- CONTENITORE PRINCIPALE DI TUTTE LE TAB -->
                    <div class="tab-content" id="entityTabsContent">
                        
                        <!-- TAB PERSONE -->
                        <div class="tab-pane fade show active" id="people-pane" role="tabpanel" aria-labelledby="people-tab" tabindex="0">
                            <div class="row w-100 m-0 justify-content-center card-holder">

                                <xsl:apply-templates select="//tei:profileDesc/tei:particDesc/tei:listPerson/tei:person" />

                            </div>
                        </div>

                        <!-- TAB LUOGHI -->
                        <div class="tab-pane fade" id="places-pane" role="tabpanel" aria-labelledby="places-tab" tabindex="0">
                            <div class="row w-100 m-0 justify-content-center card-holder">

                                <xsl:apply-templates select="//tei:profileDesc/tei:settingDesc/tei:listPlace/tei:place" />

                            </div>
                        </div>

                        <!-- TAB EVENTI -->
                        <div class="tab-pane fade" id="events-pane" role="tabpanel" tabindex="0">
                            <div class="row w-100 m-0 justify-content-center card-holder">
                            
                                <xsl:apply-templates select="//tei:profileDesc/tei:settingDesc/tei:listEvent/tei:event" />

                            </div>
                        </div>

                        <!-- TAB ARTWORKS -->
                        <div class="tab-pane fade" id="artworks-pane" role="tabpanel" tabindex="0">
                            <div class="row w-100 m-0 justify-content-center card-holder">
                            
                                <xsl:apply-templates select="//tei:profileDesc/tei:particDesc/tei:listObject/tei:object" />

                            </div>
                        </div>

                        <!-- TAB ORGANIZATIONS -->
                        <div class="tab-pane fade" id="organizations-pane" role="tabpanel" tabindex="0">
                            <div class="row w-100 m-0 justify-content-center card-holder">
                            
                                <xsl:apply-templates select="//tei:profileDesc/tei:particDesc/tei:listOrg/tei:org" />

                            </div>
                        </div>
                
                    </div>
                    
                    

                    <div class="row w-100">
                        <div class="container">
                            <h2 class="text-purple-title text-center mb-5">RELATIONS TABLE</h2>
                        </div>
                    </div>  
                    
                    
                    <xsl:apply-templates select="//tei:listRelation" />

                </div>
                <!-- ==== FINE TABS ==== -->



             <!-- JAVASCRIPT -->
                <script>
                    function flipCard(cardId) {
                    const card = document.getElementById(cardId);
                    card.classList.toggle('is-flipped');
                    }

                    function switchLanguage(cardId, lang, clickedButton) {
                    const textIt = document.getElementById('text-it-' + cardId);
                    const textEn = document.getElementById('text-en-' + cardId);
                    const title = document.getElementById('title-' + cardId);

                    if (lang === 'it') {
                        textIt.classList.remove('d-none');
                        textEn.classList.add('d-none');
                        title.innerText = "Descrizione";
                    } else if (lang === 'en') {
                        textIt.classList.add('d-none');
                        textEn.classList.remove('d-none');
                        title.innerText = "Description";
                    }

                    // Gestione dello stile dei bottoni attivi
                    const buttonGroup = clickedButton.parentElement;
                    const allButtons = buttonGroup.querySelectorAll('.btn-lang');
                    allButtons.forEach(btn => btn.classList.remove('active'));
                    
                    clickedButton.classList.add('active');
                    }
                </script>

                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="tei:persName | tei:objectName | tei:orgName | tei:title | tei:rs | tei:placeName">
        <xsl:variable name="entity_id">
            <xsl:value-of select="@ref"/>
        </xsl:variable>
            
        <span class="purple-highlight text-entity" title="Entity ID: {$entity_id}">
            <xsl:choose>
                <xsl:when test="self::tei:title">  <!-- if the current node is a title, then emphasize it -->
                    <em><xsl:apply-templates/></em>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates/>
                </xsl:otherwise>
            </xsl:choose>
        </span>
        
    </xsl:template>
    
    <xsl:template match="tei:ptr">
        <sup class="note-size">
            <xsl:value-of select="@n"/>
        </sup>
    </xsl:template>
    
    <xsl:template match="tei:gap[@reason='omitted']">
        <xsl:text>[...]</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:foreign">
        <em><xsl:apply-templates/></em>
    </xsl:template>
    
    <xsl:template match="tei:quote">
        « <em><xsl:apply-templates/></em> »
    </xsl:template>

    <!-- Creating template for the sources cards -->
    <xsl:template match="tei:listBibl[@type='sources']">
        <xsl:for-each select="//tei:listBibl[@type='sources']/tei:biblStruct">

            <!-- Creating a dynamic id for each source -->
            <xsl:variable name="cardID" select="concat('source_', position())" />

            <div class="col-lg-6 d-flex justify-content-center mb-5 mb-lg-0">
                <div class="flip-card card-width-custom">

                    <!-- Assigning the dynamic id -->
                    <div class="flip-card-inner" id="{$cardID}">

                        <!-- Modeling the front of the card -->
                        <div class="flip-card-front card-surface p-4">
                            <div class="card-body d-flex flex-column">  
                                <div class="my-auto">
                                    <h3 class="card-title text-purple-title text-center mb-4"><xsl:value-of select="tei:monogr/tei:title[@type='main']"/></h3>

                                    <xsl:if test="tei:monogr/tei:title[@type='sub']">
                                        <h6 class="mb-3 text-light"><strong class="purple-highlight">Subtitle: </strong> <xsl:value-of select="tei:monogr/tei:title[@type='sub']"/></h6>
                                    </xsl:if>

                                    
                                    <h6 class="mb-3 text-light"><strong class="purple-highlight">Author:</strong><xsl:value-of select="tei:monogr/tei:author"/></h6>
                                    <h6 class="mb-3 text-light"><strong class="purple-highlight">Publication year: </strong> <xsl:value-of select="tei:monogr/tei:imprint/tei:date"/></h6>
                                    <h6 class="mb-3 text-light"><strong class="purple-highlight">Publisher: </strong> <xsl:value-of select="tei:monogr/tei:imprint/tei:publisher"/></h6>
                                    <h6 class="mb-3 text-light"><strong class="purple-highlight">Publication place: </strong> <xsl:value-of select="tei:monogr/tei:imprint/tei:pubPlace"/></h6>
                                    <h6 class="mb-3 text-light"><strong class="purple-highlight">ISBN: </strong> <xsl:value-of select="tei:monogr/tei:idno[@type='ISBN']"/></h6>
                                    <h6 class="mb-0 text-light"><strong class="purple-highlight">Language: </strong> <xsl:value-of select="tei:monogr/tei:textLang"/></h6>

                                </div>    

                                <div class="mt-auto pt-4">
                                    <button class="btn btn-purple w-100" onclick="flipCard('{$cardID}')">Read Description</button>
                                </div>
                            </div>
                        </div>

                        <!-- Modeling the back of the card -->

                        <div class="flip-card-back card-surface p-4 custom-scroll">
                            <div class="card-body d-flex flex-column align-items-center">
                                <h4 class="text-purple-title mb-2" id="title-{$cardID}">Description</h4>
                                <div class="btn-group btn-group-sm mb-3" role="group">
                                    <button type="button" class="btn btn-outline-light btn-lang active" onclick="switchLanguage('{$cardID}', 'en', this)">EN</button>
                                    <button type="button" class="btn btn-outline-light btn-lang" onclick="switchLanguage('{$cardID}', 'it', this)">IT</button>
                                </div>

                                <p id="text-en-{$cardID}" class="text-light w-100">
                                    <xsl:value-of select="tei:note[@xml:lang='en']"/>
                                </p>
                                <p id="text-it-{$cardID}" class="text-light d-none w-100">
                                    <xsl:value-of select="tei:note[@xml:lang='it']"/>
                                </p>

                                <div class="mt-auto pt-4 text-center w-100">
                                    <button class="btn btn-outline-light w-100" onclick="flipCard('{$cardID}')">Back to Details</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>    
        </xsl:for-each>
    </xsl:template>

    <!-- Creating template for the snippets -->
    <xsl:template match="tei:div[@type='excerpts']">

            <h4 class="text-light mb-5 mt-5">
                <xsl:value-of select="tei:head"/>
            </h4>
            
            <!-- Looping through each snippet -->
            <xsl:for-each select="tei:div[@type='snippet']">

                <div class="container mt-5">
                        <div class="row border-start border-4 quote">
                            <p class="mb-0">
                                <xsl:apply-templates select="tei:p"/>
                            </p>
                        </div>
                    
                    <div class="text-secondary mt-2">

                        <!-- Check if the the snippet is a footnote or not -->
                        <xsl:if test="tei:p/tei:note">
                            <p class="mb-1 small">
                                Footnote <xsl:value-of select="tei:p/tei:note/@n"/>
                            </p>
                        </xsl:if>
                        <!-- Check if the the snippet is contained in one or more pages -->
                        
                        <p class="mb-0">
                            <xsl:choose>
                                <xsl:when test="contains(tei:pb/@n, '-')">
                                    <xsl:text>Pages </xsl:text>
                                </xsl:when>

                                <xsl:otherwise>
                                    <xsl:text>Page </xsl:text>
                                </xsl:otherwise>
                            </xsl:choose>

                            <xsl:value-of select="tei:pb/@n"/>
                        </p>
                        
                    </div>
                </div>
            </xsl:for-each>
    </xsl:template>

    <!--  =============== TEMPLATE FOR CARDS OF PEOPLE IN TABS  =============  -->
    <xsl:template name="tab-card">

        <!-- defining the parameters of the template -->
        <xsl:param name="entity_id" />
        <xsl:param name="entity_name" />
        <xsl:param name="entity_variant_name" select="/.." />
        <xsl:param name="entity_standard_name" select="/.." />
        <xsl:param name="entity_alternative_name" select="/.." />
        <xsl:param name="entity_abbrev_name"  select="/.."/>
        <xsl:param name="button_text" select="'See details'" /> <!-- default value -->
        <xsl:param name="idno_nodes" select="/.." />
        <xsl:param name="en_desc" />
        <xsl:param name="it_desc" />
        

        <!-- for the front of the card -->
        <div class="col-sm-6 col-lg-4 col-xl-3 d-flex justify-content-center mb-5">
            <div class="sm-flip-card sm-card-width-custom">
                <div class="flip-card-inner" id="{$entity_id}">

                    <div class="flip-card-front card-surface p-4">
                        <div class="card-body d-flex flex-column text-center">
                            <div class="my-auto">

                                <h3 class="card-title text-purple-title mb-4">
                                    <xsl:value-of select="$entity_name"/>
                                </h3>

                                <!-- Name variations for organizations -->
                                <xsl:if test="$entity_standard_name">
                                    <h6 class="mb-2 text-light">
                                        <strong class="purple-highlight">Std. name: </strong>
                                        <xsl:value-of select="$entity_standard_name"/>
                                    </h6>   
                                </xsl:if>


                                <xsl:for-each select="$entity_alternative_name">
                                    <xsl:if test="@xml:lang='en'">
                                        <h6 class="mb-3 text-light">
                                            <strong class="purple-highlight">Alt. name: 
                                            </strong>
                                            <xsl:value-of select="."/>
                                        </h6>
                                    </xsl:if>
                                </xsl:for-each>    
                                
                                <!--
                                <xsl:if test="$entity_abbrev_name">
                                    <h6 class="mb-2 text-light">
                                        <strong class="purple-highlight">Abbr. name: </strong>
                                        <xsl:value-of select="$entity_abbrev_name"/>
                                    </h6>
                                </xsl:if>  -->

                                <!-- PARAMETERS ARTWORKS -->
                                
                                <xsl:if test="$entity_variant_name">
                                    <h6 class="mb-2 text-light">
                                        <strong class="purple-highlight">Variant names: </strong>
                                        <xsl:for-each select="$entity_variant_name">
                                            <xsl:value-of select="."/>
                                            <xsl:if test="position() != last()">, </xsl:if>
                                        </xsl:for-each>
                                    </h6>
                                </xsl:if>


                                <xsl:if  test="$idno_nodes">
                                    
                                    <!-- inserting ids -->
                                    <xsl:for-each select="$idno_nodes">
                                        <h6 class="mb-2 text-light">
                                            <strong class="purple-highlight"><xsl:value-of select="@type" />: </strong>
                                            
                                            <!-- Creating a variable for the prefix uri -->
                                            <xsl:variable name="base_url">
                                                <xsl:choose>
                                                    <xsl:when test="@type = 'viaf'" >
                                                        <xsl:text>https://viaf.org/viaf/</xsl:text>
                                                    </xsl:when>
                                                    <xsl:when test="@type = 'wikidata'" >
                                                        <xsl:text>https://www.wikidata.org/wiki/</xsl:text>
                                                    </xsl:when>
                                                    <xsl:when test="@type = 'GeoNames'" >
                                                        <xsl:text>https://sws.geonames.org/</xsl:text>
                                                    </xsl:when>
                                                </xsl:choose>
                                            </xsl:variable>    
                                                
                                                
                                            <a href="{concat($base_url, .)}" target="_blank" class="text-decoration-none me-2">
                                                <xsl:value-of select="."/>
                                            </a>
                                        </h6>
                                    </xsl:for-each>
                                </xsl:if>

                            </div>

                            <!-- id entity on screen -->
                            <div class="text-center mb-3">
                                <code class="text-light bg-dark px-2 py-1 rounded card-id-size">
                                    #<xsl:value-of select="$entity_id"/>
                                </code>
                            </div>

                            <div class="mt-auto pt-4">
                                <button class="btn btn-purple w-100" onclick="flipCard('{$entity_id}')">Read Description</button>
                            </div>
                        </div>
                    </div>
                    <!-- for the back of the card -->
                    <div class="flip-card-back card-surface p-4 custom-scroll">
                        <div class="card-body d-flex flex-column align-items-center">
                            <h4 class="text-purple-title mb-2" id="title-{$entity_id}">Description</h4>

                            <div class="btn-group btn-group-sm mb-3" role="group">
                                <button type="button" class="btn btn-outline-light btn-lang active" onclick="switchLanguage('{$entity_id}', 'en', this)">EN</button>
                                <button type="button" class="btn btn-outline-light btn-lang" onclick="switchLanguage('{$entity_id}', 'it', this)">IT</button>
                            </div>

                            <p id="text-en-{$entity_id}" class="text-light w-100" style="font-size: 0.95rem;">
                                <xsl:value-of select="$en_desc"/>
                            </p>
                            <p id="text-it-{$entity_id}" class="text-light w-100 d-none" style="font-size: 0.95rem;">
                                <xsl:value-of select="$it_desc"/>
                            </p>

                            <div class="mt-auto pt-3 text-center w-100">
                                <button class="btn btn-outline-light w-100" onclick="flipCard('{$entity_id}')">Back to Details</button>
                            </div>
                        </div>    
                    </div>
                </div>
            </div>    
        </div>
    </xsl:template>

    <!--  TEMPLATE FOR PEOPLE ENTITIES -->
    <xsl:template match="tei:person">
        <xsl:call-template name="tab-card">
            <xsl:with-param name="entity_id" select="@xml:id" />
            <xsl:with-param name="entity_name" select="tei:persName" />
            <xsl:with-param name="button_text" select="'See details'" /> 
            <xsl:with-param name="idno_nodes" select="tei:idno" />
            <xsl:with-param name="en_desc" select="tei:note[@xml:lang='en']" />
            <xsl:with-param name="it_desc" select="tei:note[@xml:lang='it']" /> 
        </xsl:call-template>
    </xsl:template>
    
    <!--  TEMPLATE FOR PLACES ENTITIES -->
    <xsl:template match="tei:place">
        <xsl:call-template name="tab-card">
            <xsl:with-param name="entity_id" select="@xml:id" />
            <xsl:with-param name="entity_name" select="tei:placeName" />
            <xsl:with-param name="button_text" select="'See details'" /> 
            <xsl:with-param name="idno_nodes" select="tei:idno" />
            <xsl:with-param name="en_desc" select="tei:note[@xml:lang='en']" />
            <xsl:with-param name="it_desc" select="tei:note[@xml:lang='it']" /> 
        </xsl:call-template>
    </xsl:template>

    <!--  TEMPLATE FOR EVENT ENTITIES -->
    <xsl:template match="tei:event">
        <xsl:call-template name="tab-card">
            <xsl:with-param name="entity_id" select="@xml:id" />
            <xsl:with-param name="entity_name" select="tei:label" />
            <xsl:with-param name="button_text" select="'See details'" /> 
            <xsl:with-param name="en_desc" select="tei:desc[@xml:lang='en']" />
            <xsl:with-param name="it_desc" select="tei:desc[@xml:lang='it']" /> 
        </xsl:call-template>
    </xsl:template>

    <!--  TEMPLATE FOR ORGANIZATIONS ENTITIES -->
    <xsl:template match="tei:org">
        <xsl:call-template name="tab-card">
            <xsl:with-param name="entity_id" select="@xml:id" />
            <xsl:with-param name="entity_name" select="tei:orgName[@type='official']" />
            <xsl:with-param name="entity_standard_name" select="tei:orgName[@type='standard']" />
            <xsl:with-param name="entity_alternative_name" select="tei:orgName[@type='alt']" />
            <xsl:with-param name="entity_abbrev_name" select="tei:orgName[@type='abbrev']" />
            <xsl:with-param name="button_text" select="'See details'" /> 
            <xsl:with-param name="idno_nodes" select="tei:idno" />
            <xsl:with-param name="en_desc" select="tei:note[@xml:lang='en']" />
            <xsl:with-param name="it_desc" select="tei:note[@xml:lang='it']" /> 
        </xsl:call-template>
    </xsl:template>

    <!--  TEMPLATE FOR ARTOWORKS ENTITIES -->
    <xsl:template match="tei:object">
        <xsl:call-template name="tab-card">
            <xsl:with-param name="entity_id" select="@xml:id" />
            <xsl:with-param name="entity_name" select=".//tei:objectName[@type='preferred'] | .//tei:objectName[not(@type)]" />
            <xsl:with-param name="entity_variant_name" select=".//tei:objectName[@type='variant']" />
            <xsl:with-param name="button_text" select="'See details'" /> 
            <xsl:with-param name="idno_nodes" select="tei:idno"/>
            <xsl:with-param name="en_desc" select="tei:note[@xml:lang='en']" />
            <xsl:with-param name="it_desc" select="tei:note[@xml:lang='it']" /> 
        </xsl:call-template>
    </xsl:template>
    
    <xsl:template match="tei:listRelation">
        <div class="container">
            <div class="table-responsive custom-table-wrapper rounded mt-4">
                <table class="table table-striped-columns  table-dark table-hover mb-0 text-center">
                    <!-- INTESTAZIONE TABELLA -->
                    <thead>
                        <tr class="table-header-purple">
                            <th scope="col" class="py-3 px-4">Entity 1 (Subject)</th>
                            <th scope="col" class="py-3 px-4">Type of relation (Predicate)</th>
                            <th scope="col" class="py-3 px-4">Entity 2 (Object)</th>
                        </tr>
                    </thead>
                    
                    <tbody>
                        <xsl:for-each select="tei:relation">
                            <tr>
                                <td class="py-3 px-4">
                                    <code class=" bg-dark px-2 py-1 rounded"><xsl:value-of select="@active"/></code>    
                                </td>
                                <td class="py-3 px-4">
                                    <span class="px-3 py-2"><xsl:value-of select="@name"/></span>
                                </td>
                                <td class="py-3 px-4"><code class="bg-dark px-2 py-1 rounded"><xsl:value-of select="@passive"/></code></td>
                            </tr>
                        </xsl:for-each>
                        
                    </tbody>
                </table>
            </div>
        </div>     
        
    </xsl:template>
    
</xsl:stylesheet>



## Master Canonical Rules for Mobile Card Games with Text

Based on extensive research across mobile game design, accessibility standards, usability heuristics, and successful card game implementations, here is the definitive set of **54 Master Canonical Rules** organized into 12 core categories. These rules represent the synthesized best practices from WCAG 2.1 AA standards, Nielsen's usability heuristics, Game Accessibility Guidelines, and proven design patterns from successful mobile card games.

***

## I. Typography Rules (5 Rules)

### Rule 1: Minimum Font Size Standard ⚠️ CRITICAL
**Requirement:** Body text must be minimum 14-16pt for primary card content[1][2][3]

**Rationale:** Ensures readability at arm's length on mobile devices. Text smaller than this creates accessibility barriers and forces players to bring cards uncomfortably close to their face.[4][1]

### Rule 2: Typography Hierarchy System ⚠️ CRITICAL
**Requirement:** Implement 5-level hierarchy:
- Primary Headlines: 24-32pt (main card titles, important actions)
- Secondary Headings: 18-24pt (section headers, card categories)
- Body Text: 14-16pt (card descriptions, main content)
- Supporting Text: 12-14pt (stats, metadata)
- Fine Print: 10-12pt (legal text, timestamps - use sparingly)[3][5][1]

**Rationale:** Establishes clear information hierarchy for rapid comprehension and scanning. Players process cards in seconds and need immediate understanding of importance levels.[5]

### Rule 3: Scalable Units Required ⚠️ CRITICAL
**Requirement:** Use density-independent pixels (dp/sp) on Android, points on iOS - never fixed pixels[6][1][3]

**Rationale:** Screen densities range from 150-400+ PPI on modern smartphones. Fixed pixel sizes appear drastically different across devices, while scalable units ensure consistent appearance.[3]

### Rule 4: Font Weight and Contrast ⚠️ CRITICAL
**Requirement:** Minimum 4.5:1 contrast ratio for normal text, 3:1 for large text (18pt+)[7][5]

**Rationale:** WCAG 2.1 AA compliance requirement. Proper contrast ensures readability across visual conditions and impairments.[5][7]

### Rule 5: Consistent Typography System ⚠️ CRITICAL
**Requirement:** Once established, typography sizes must remain consistent throughout entire game interface[8][9]

**Rationale:** Consistency allows players to subconsciously learn the visual language, making navigation feel natural and intuitive.[9][8]

***

## II. Touch Interface Rules (4 Rules)

### Rule 6: Minimum Touch Target Size ⚠️ CRITICAL
**Requirement:** 
- 24×24 pixels: Absolute minimum (Level AA)
- 44×44 pixels: Recommended (Level AAA)
- 48×48 pixels: Optimal[10][11][6]

**Rationale:** 48×48 pixels corresponds to approximately 9mm—the size of an average finger pad. This ensures reliable interaction without accidental activation.[12][11]

### Rule 7: Touch Target Spacing ⚠️ CRITICAL
**Requirement:** Minimum 8 pixels spacing between interactive elements both horizontally and vertically[11]

**Rationale:** Prevents accidental activation of adjacent elements, particularly crucial in card games where multiple interactive elements appear in close proximity.[13][11]

### Rule 8: Entire Card Clickability ⚠️ CRITICAL
**Requirement:** Make entire card area interactive, not just small buttons within cards[14]

**Rationale:** Dramatically improves usability and reduces frustration. Players shouldn't need to precisely target small regions within a card.[14]

### Rule 9: Pointer Cancellation ⚠️ CRITICAL
**Requirement:** Allow users to cancel tap/click by moving away from target before releasing[15]

**Rationale:** Reduces errors from involuntary motion or accidental touches. Players must be able to abort actions before completing them.[15]

---

## III. Card Layout Rules (4 Rules)

### Rule 10: Three Pillars of Card Design ⚠️ CRITICAL
**Requirement:** Follow:
1. **Visibility** - Most important information accessible even when cards are stacked/obscured
2. **Hierarchy** - Arrange information from most to least important
3. **Brevity** - Use keywords/icons instead of repeated phrases[16][17]

**Rationale:** Core principles for effective card information architecture that work in physical and digital contexts.[17][16]

### Rule 11: Information Density Limit ⚠️ CRITICAL
**Requirement:** Maximum 2-3 lines of body text per card; more requires tooltips or expandable areas[4]

**Rationale:** Players tend to ignore text-heavy cards. Short, focused text reduces cognitive load and improves comprehension.[4][5]

### Rule 12: Keyword System Implementation ⚠️ CRITICAL
**Requirement:** Recurring phrases or mechanics must be converted to symbols/keywords[18][16]

**Rationale:** Saves precious screen space, reduces reading time, and lowers cognitive load through pattern recognition.[18][16]

### Rule 13: Card Readability at Distance ⚠️ CRITICAL
**Requirement:** Card text should be readable at arm's length (minimum 2mm character height for physical, 14pt digital equivalent)[4]

**Rationale:** Players need to read cards without bringing them uncomfortably close to their face.[4]

***

## IV. Color Accessibility Rules (3 Rules)

### Rule 14: No Color-Only Information ⚠️ CRITICAL
**Requirement:** Never convey essential information through color alone; always provide second channel (icons, patterns, shapes, labels)[19][20][7]

**Rationale:** 8% of males and 1% of females have color vision deficiency. Color filters rarely help; second channels ensure universal access.[20][7][19]

### Rule 15: Customizable UI Colors
**Requirement:** Provide UI color customization options (minimum: preset themes, optimal: full RGB selection)[19]

**Rationale:** Most effective accessibility solution for color vision differences. Players can modify colors to create distinctions that work for their specific vision.[19]

### Rule 16: Text Contrast Requirements ⚠️ CRITICAL
**Requirement:** Maintain minimum 4.5:1 contrast ratio; use semi-transparent overlays or text shadows over complex backgrounds[7][5]

**Rationale:** Ensures consistent readability regardless of underlying imagery or background complexity.[5]

***

## V. Nielsen's 10 Usability Heuristics Applied to Games (10 Rules)

### Rule 17: Visibility of System Status ⚠️ CRITICAL
**Requirement:** Always keep players informed about game state through appropriate feedback within reasonable time[12]

**Rationale:** Players need to know if interactions succeeded, current health/resources, turn state, and available actions.[12]

### Rule 18: Match Between System and Real World ⚠️ CRITICAL
**Requirement:** Use familiar language, terms, and concepts; follow real-world conventions for information ordering[12]

**Rationale:** Reduces cognitive load by leveraging existing mental models. Unfamiliar terminology increases learning curve.[12]

### Rule 19: User Control and Freedom ⚠️ CRITICAL
**Requirement:** Provide clearly marked undo/redo options for reversible actions[12]

**Rationale:** Users make mistakes; allow easy recovery without extended dialogue or punishment.[12]

### Rule 20: Consistency and Standards ⚠️ CRITICAL
**Requirement:** Follow platform conventions; users should not wonder if different words/actions mean same thing[12]

**Rationale:** Years of game design have established standards. Breaking them forces relearning and increases errors.[12]

### Rule 21: Error Prevention ⚠️ CRITICAL
**Requirement:** Use confirmation dialogs for irreversible actions; prevent errors before they occur[12]

**Rationale:** Prevention better than recovery. Confirmation dialogs particularly important for destructive actions like deleting decks.[12]

### Rule 22: Recognition Rather Than Recall ⚠️ CRITICAL
**Requirement:** Make objects, actions, and options visible; provide context-sensitive controls[12]

**Rationale:** Minimizes memory load by showing relevant information when needed rather than requiring players to remember.[12]

### Rule 23: Flexibility and Efficiency of Use
**Requirement:** Provide accelerators (shortcuts, hotkeys, customization) for experienced users while keeping interface simple for novices[12]

**Rationale:** Serves both novice and expert users effectively. Power users want efficiency; newcomers want simplicity.[12]

### Rule 24: Aesthetic and Minimalist Design ⚠️ CRITICAL
**Requirement:** Display only relevant information; use progressive disclosure for secondary information[12]

**Rationale:** Irrelevant information competes with relevant information and diminishes its visibility. Every element should serve a purpose.[12]

### Rule 25: Error Recovery Support ⚠️ CRITICAL
**Requirement:** Error messages in plain language, precisely indicating problem with constructive solution[12]

**Rationale:** Helps users understand and recover from errors quickly without frustration.[12]

### Rule 26: Help and Documentation
**Requirement:** Provide searchable, task-focused help with concrete steps; accessible but not required for basic play[12]

**Rationale:** Complex card games need accessible documentation for forgotten interactions without interrupting play flow.[12]

---

## VI. Performance Rules (3 Rules)

### Rule 27: 150 Draw Call Limit ⚠️ CRITICAL
**Requirement:** Keep total draw calls under 150 per frame for mid-range device compatibility[21][22]

**Rationale:** Ensures smooth 60fps performance on target devices. Exceeding this causes frame drops and stuttering.[22][21]

### Rule 28: Texture Optimization ⚠️ CRITICAL
**Requirement:** Use power-of-two texture dimensions; ASTC compression; UI atlases for combined elements[22]

**Rationale:** Reduces memory usage and improves rendering performance. UI atlases dramatically reduce draw calls.[21][22]

### Rule 29: Animation Performance Priority ⚠️ CRITICAL
**Requirement:** Prioritize smooth simple animations over complex effects that cause frame drops[23][22]

**Rationale:** Consistent frame rate provides better user experience than visual complexity with stuttering.[22]

***

## VII. Responsive Design Rules (3 Rules)

### Rule 30: Multi-Device Adaptation ⚠️ CRITICAL
**Requirement:** Interface must adapt to different screen sizes and orientations (portrait/landscape)[24][25]

**Rationale:** Players use variety of devices with different aspect ratios. Design must be flexible.[25][24]

### Rule 31: 200% Zoom Support ⚠️ CRITICAL
**Requirement:** Interface must remain functional and legible at 200% zoom level[15]

**Rationale:** Supports low vision users and system magnification tools. WCAG 2.1 AA requirement.[15]

### Rule 32: Grid-Based Layout System ⚠️ CRITICAL
**Requirement:** Use grid-based layouts for consistent spacing and alignment across devices[25][14]

**Rationale:** Provides predictable, scalable layout structure that adapts gracefully.[14][25]

---

## VIII. Game-Specific Heuristics (5 Rules)

### Rule 33: Interactive Tutorial Required ⚠️ CRITICAL
**Requirement:** Provide interactive tutorial that is skippable for experienced players[26][27]

**Rationale:** Not all players know how to play. Tutorials accelerate onboarding, but forcing experienced players through them creates frustration.[27][26]

### Rule 34: Control Remapping ⚠️ CRITICAL
**Requirement:** Allow controls to be remapped/reconfigured[28][27]

**Rationale:** Accommodates motor impairments and personal preferences. Essential for accessibility.[28][27]

### Rule 35: Adjustable Game Speed
**Requirement:** Include option to adjust game speed/pace[27][28]

**Rationale:** Benefits cognitive and motor accessibility. Players with different abilities need different pacing.[28][27]

### Rule 36: Save State Management ⚠️ CRITICAL
**Requirement:** Support player interruption with autosave and manual save in multiple states[29][27]

**Rationale:** Mobile context requires ability to pause/resume anytime. Players get interrupted frequently.[29][27]

### Rule 37: Objective Indicators ⚠️ CRITICAL
**Requirement:** Provide clear indication/reminder of current objectives during gameplay[29][27]

**Rationale:** Reduces cognitive load. Essential for players who return after interruptions.[27][29]

---

## IX. Information Architecture Rules (3 Rules)

### Rule 38: Spatial Logic Consistency
**Requirement:** Follow left-to-right temporal progression (past-present-future) in layout[30]

**Rationale:** Leverages natural reading patterns for intuitive understanding. Deck (past) → Play area (present) → Discard/future actions (right).[30]

### Rule 39: Physical Metaphor Application
**Requirement:** Use physical card game metaphors (weight, inertia, tactile feedback) where appropriate[31][32]

**Rationale:** Makes digital interactions feel natural and familiar. Hearthstone's success stems from this principle.[32][31]

### Rule 40: Progressive Disclosure ⚠️ CRITICAL
**Requirement:** Show only task-relevant information; hide secondary details in tooltips/expandable areas[30][12]

**Rationale:** Reduces cognitive overload while maintaining access to detailed information when needed.[30][12]

***

## X. Seven UI Design Essentials (6 Rules)

### Rule 41: Clarity ⚠️ CRITICAL
**Requirement:** UI elements must be immediately understandable without ambiguity[33]

**Rationale:** Foundation of good mobile game UI design. Confusion leads to abandonment.[33]

### Rule 42: Discriminability ⚠️ CRITICAL
**Requirement:** Interactive elements must be clearly distinguishable from non-interactive elements[33][27]

**Rationale:** Players must know what they can interact with. Give clear indication that interactive elements are interactive.[33][27]

### Rule 43: Conciseness ⚠️ CRITICAL
**Requirement:** Communicate information efficiently with minimal text/elements[29][33]

**Rationale:** Limited screen space demands economy of expression. Brevity improves comprehension.[33][29]

### Rule 44: Detectability ⚠️ CRITICAL
**Requirement:** Important UI elements must be easily found without searching[29][33]

**Rationale:** Critical information shouldn't be hidden or hard to locate. Players scan interfaces rapidly.[33][29]

### Rule 45: Legibility ⚠️ CRITICAL
**Requirement:** All text must be readable in expected viewing conditions[29][33]

**Rationale:** Illegible text renders information useless. Must work in varied lighting conditions.[33][29]

### Rule 46: Comprehensibility ⚠️ CRITICAL
**Requirement:** Interface meaning and function must be immediately graspable[29][33]

**Rationale:** Players should intuit how to use interface without instruction. Simplicity enables this.[33][29]

---

## XI. Testing and Iteration Rules (3 Rules)

### Rule 47: Accessibility User Testing
**Requirement:** Include people with impairments (colorblind, motor, visual, cognitive) in playtesting[34][28][27]

**Rationale:** Real user feedback reveals issues development team cannot anticipate. Testing assumptions prevents exclusion.[34][28][27]

### Rule 48: Multi-Device Testing ⚠️ CRITICAL
**Requirement:** Test on range of devices including low-end hardware, various screen sizes, and different OS versions[34][28]

**Rationale:** Ensures compatibility across target device spectrum. Performance varies dramatically.[28][34]

### Rule 49: Analytics-Informed Design
**Requirement:** Use analytics data to inform interface decisions based on actual player behavior[23]

**Rationale:** Reveals how players actually interact versus design assumptions. Data drives better decisions.[23]

---

## XII. Card UI Specific Rules (5 Rules)

### Rule 50: Card Size Adaptation
**Requirement:** Square cards for mobile portrait, rectangular cards for landscape/tablet[35][25]

**Rationale:** Optimizes screen space usage for different form factors and viewing contexts.[35][25]

### Rule 51: Rounded Corners
**Requirement:** Use rounded corners on cards for more visually appealing, relaxed feel[35]

**Rationale:** Creates more comfortable, friendly visual design. Sharp corners feel harsh.[35]

### Rule 52: High-DPI Image Support ⚠️ CRITICAL
**Requirement:** Use images optimized for high-DPI screens to avoid pixelation[35]

**Rationale:** Modern devices have high pixel density (300+ PPI). Low-resolution images look unprofessional.[35]

### Rule 53: Animation Restraint
**Requirement:** Limit animated elements; use one animated feature per card maximum[35]

**Rationale:** Too many animations create cluttered, overwhelming experience and hurt performance.[35]

### Rule 54: Stacked Card Readability ⚠️ CRITICAL
**Requirement:** Design cards so critical information (title, cost, key stats) remains visible when partially obscured[16][17]

**Rationale:** Cards often appear stacked or overlapped in hand/play area. Visibility principle is paramount.[17][16]

---

## Summary Statistics

**Total Canonical Rules:** 54
**Critical Rules:** 43 (80%)
**Recommended Rules:** 11 (20%)

These 54 rules synthesize research from WCAG 2.1 AA standards, Nielsen's usability heuristics, Game Accessibility Guidelines, successful card game implementations like Hearthstone and Legends of Runeterra, mobile UI/UX best practices, and extensive academic research on mobile game usability.[36][37][38][39][40][41][42][43][44][31][32][27][15][29][33][12]

**Critical rules (⚠️)** represent non-negotiable requirements that directly impact accessibility, usability, or performance. Violating these creates barriers for significant user populations or causes functional failures.

**Recommended rules** represent best practices that enhance user experience but can be adapted based on specific game requirements and constraints.

[1](https://www.toptal.com/designers/typography/typography-for-mobile-apps)
[2](https://www.reddit.com/r/UI_Design/comments/180yv87/what_is_the_correct_font_size_for_mobile_apps/)
[3](https://thisisglance.com/learning-centre/how-do-i-choose-the-right-font-size-for-my-mobile-app)
[4](https://danielsolisblog.blogspot.com/2011/11/5-graphic-design-and-typography-tips.html)
[5](https://indieklem.com/13-the-basics-of-typography-in-game-interface/)
[6](https://support.google.com/accessibility/android/answer/7101858?hl=en)
[7](https://dev.to/indieklem/how-to-make-our-game-colors-accessible-to-everyone-8cb)
[8](https://aaagameartstudio.com/blog/mobile-games-ui-ux)
[9](https://www.andacademy.com/resources/blog/ui-ux-design/game-ui-design/)
[10](https://dequeuniversity.com/rules/axe/4.10/target-size)
[11](https://web.dev/articles/accessible-tap-targets)
[12](https://www.nngroup.com/articles/usability-heuristics-applied-video-games/)
[13](https://www.reddit.com/r/gamedesign/comments/1c8h8sv/ui_design_for_a_card_game_how_can_i_fit_two/)
[14](https://www.justinmind.com/ui-design/cards)
[15](https://www.filamentgames.com/blog/accessibility-terms-for-game-developers-a-wcag-2-1-aa-glossary/)
[16](https://danielsolisblog.blogspot.com/2024/02/three-principles-of-card-design.html)
[17](https://www.mattpaquette.com/design-blog/2018/7/9/tabletop-graphic-design-card-framworks-101)
[18](https://www.youtube.com/watch?v=XDd4u2xnRtE)
[19](https://www.reddit.com/r/gamedev/comments/10zgxg9/hi_game_developers_colorblind_person_here_please/)
[20](https://mashable.com/article/colorblindness-video-games-accessibility)
[21](https://www.youtube.com/watch?v=hGcvEZOUmYo)
[22](https://www.wayline.io/blog/unity-mobile-game-optimization-checklist)
[23](https://moldstud.com/articles/p-key-strategies-to-enhance-the-user-interface-of-your-mobile-game-for-maximum-performance-efficiency)
[24](https://allclonescript.com/blog/card-game-app-ui-design-kits)
[25](https://uxdesign.cc/8-best-practices-for-ui-card-design-898f45bb60cc)
[26](https://games.themindstudios.com/post/card-game-development/)
[27](https://gameaccessibilityguidelines.com/full-list/)
[28](https://www.gamedeveloper.com/game-platforms/accessibility-heuristics-and-evaluation-criteria-for-mobile-games)
[29](https://www.espjournals.org/IJCEET/2024/Volume2-Issue1/IJCEET-V2I1P103.pdf)
[30](https://gdkeys.com/the-card-games-ui-design-of-fairtravel-battle/)
[31](https://www.behance.net/gallery/25695693/Hearthstone-UI)
[32](https://www.youtube.com/watch?v=axkPXCNjOh8)
[33](https://pixune.com/blog/mobile-games-ui-design-a-handy-guide/)
[34](https://www.keywordsstudios.com/en/about-us/news-events/news/accessibility-and-mobile-game-development/)
[35](https://www.eleken.co/blog-posts/card-ui-examples-and-best-practices-for-product-owners)
[36](https://www.sciencedirect.com/science/article/pii/S1877050919319246)
[37](https://www.w3.org/TR/wcag-3.0/)
[38](https://dl.acm.org/doi/10.1145/1152215.1152218)
[39](https://www.w3.org/TR/WCAG21/)
[40](https://gameaccessibilityguidelines.com)
[41](https://www.nngroup.com/articles/usability-heuristics-board-games/)
[42](https://accessate.net/r2277/game_accessibility_guidelines)
[43](https://masteringruneterra.com/how-to-play-legends-of-runeterra-on-your-phone/)
[44](https://www.youtube.com/watch?v=OORgmxMrchM)
[45](https://www.reddit.com/r/gamedesign/comments/zwrsy3/game_design_for_a_card_game/)
[46](https://developer.apple.com/design/human-interface-guidelines)
[47](https://www.linkedin.com/pulse/complete-guide-card-game-app-development-creatiosoft-zkecc)
[48](https://uxdesign.cc/creating-a-card-game-inside-figma-fdd25c246251)
[49](https://www.gamedeveloper.com/design/card-games---a-simple-design-is-a-good-design)
[50](https://www.linkedin.com/pulse/how-make-card-game-from-perspective-ux-designer-reena-ngauv)
[51](https://www.reddit.com/r/UI_Design/comments/10ega2g/what_are_the_most_important_elements_when/)
[52](https://printninja.com/printing-resource-center/book-game-industry-standards/design-a-card-game/)
[53](https://uxkit.minotaure.io/en/the-ux-kits/the-card-games/)
[54](https://www.gameuidatabase.com)
[55](https://troypress.com/guide-to-prototyping-card-games/)
[56](https://openforge.io/mobile-academy/guides/mobile-design/how-to-design-user-interfaces-for-mobile-games-in-figma/)
[57](https://www.dxlab.digital/post/the-world-s-first-card-game-with-a-ux-design-theme-step-into-the-role-of-a-ux-designer-have-fun-an)
[58](https://www.designrush.com/best-designs/apps/trends/mobile-design-patterns)
[59](https://www.testdevlab.com/blog/accessibility-testing-in-video-games)
[60](https://uxplaybook.org/articles/essential-interaction-design-patterns-and-techniques)
[61](https://uxdesign.cc/cheatsheet-to-the-most-common-interaction-patterns-8140dcfff43)
[62](https://afb.org/aw/summer2023/introduction-to-video-game-accessibility)
[63](https://ui-patterns.com/patterns)
[64](https://uxdesign.cc/usability-heuristics-in-game-design-29a324177d4e)
[65](https://www.interaction-design.org/literature/article/help-i-need-some-help-not-just-any-help-help-in-mobile-applications)
[66](http://uipatterns.io)
[67](https://ieeexplore.ieee.org/document/9231175/)
[68](https://www.reddit.com/r/gamedesign/comments/52zinm/card_game_rules_whats_the_complexity_sweet_spot/)
[69](https://ocw.metu.edu.tr/pluginfile.php/4129/mod_resource/content/0/ceit706_2/10/game_usability-_heuristics.pdf)
[70](https://www.reddit.com/r/truegaming/comments/17kmq6m/im_having_legibilityreadability_issues_with/)
[71](https://ablegamers.org/mobile-gaming/)
[72](https://www.uxtigers.com/post/heuristics-haikus)
[73](https://eleganthack.com/wp-content/uploads/2019/06/Game_InformationDesign.pdf)
[74](https://daily.dev/blog/10-usability-heuristics-checklist-for-ui-design)
[75](https://aura-print.com/usa/blog/post/playing-card-dimensions)
[76](https://mirigrowth.com/blog/designing-an-accessible-mobile-game/)
[77](https://www.nngroup.com/videos/video-game-design-ux/)
[78](https://www.reddit.com/r/digitalcards/comments/1gohjkl/best_digital_card_game_to_get_into_in_2024/)
[79](https://www.reddit.com/r/tabletopgamedesign/comments/vxhm76/quick_board_game_design_checklist_i_made/)
[80](https://asoworld.com/blog/mobile-game-market-trends-card-games-win-big-in-2024/)
[81](https://uxdesign.cc/board-game-ux-help-and-documentation-74335da5ce20)
[82](https://learn.microsoft.com/en-us/gaming/accessibility/developer-resources)
[83](https://help.tabletopia.com/knowledge-base/game-creator-checklist/)
[84](https://access-ability.uk/2023/01/05/1094/)
[85](https://www.pockettactics.com/best-mobile-card-games)
[86](https://checklist.gg/templates/game-design-checklist)
[87](https://rocketbrush.com/blog/mastering-mobile-game-design-tips-and-strategies)
[88](https://herotime1.com/resources/checklist-for-making-a-game/)
[89](https://legendsofelysium.io/blog/mobile-tcg-ccg-games-of-2025-digital-trading-cards-in-your-pocket/)
# Акустичний левітатор

[English](README.md) | Українська

Було спроєктовано акустичний левітатор на 40 кГц із двома увігнутими масивами та розроблено його прошивку Arduino Uno, механічну модель і чисельні розрахунки. У конструкції 72 передавальні капсулі, випаяні з HC-SR04, по 36 у кожній чаші. Форма чаш і орієнтація випромінювачів забезпечують фокусування до спільного центра.

Для конструкції було використано OpenSCAD, для акустичного поля й сил на частинку — Python, для електричної моделі — ngspice.

![Модель акустичного левітатора](results/concave_preview.png)

## Вибрана конструкція

| Параметр | Значення |
|---|---|
| Контролер | Arduino Uno, ATmega328P, 16 МГц |
| Номінальна частота / фаза масивів | 40 кГц / 0°; прошивка також підтримує 38–42 кГц і 180° |
| Живлення логіки / моста | 5 В / 9 В; обмеження струму живлення моста 1 А |
| Міст та інвертор | TB6612FNG і 74HC14 |
| Послідовний резистор кожного масиву | 22 Ом, 3 Вт |
| Корпус передавача | Приблизно 16 мм у діаметрі × 13 мм заввишки, за наявними деталями |
| Діаметр гнізда / крок у проєкції | 16,4 мм / 18 мм |
| Радіус фокуса / розміри основи | 90 мм / 220 × 158 мм |
| Акустична модель | Заданий піковий тиск у фокусі 1,5 кПа, ефективний радіус поршня 6 мм |
| Електрична модель | Прийнято 2 нФ на випромінювач; 72 нФ на масив |

Приймальні капсулі та плати далекомірів HC-SR04 до масиву не входять. Ємність випаяного передавача та допустиме безперервне збудження не визначаються специфікацією живлення модуля 5 В. Акустичний тиск та електричне навантаження вище — явно задані параметри моделі.

## Розрахунковий результат

На 40 кГц довжина хвилі становить 8,580 мм, а крок вузлів плоскої хвилі — 4,290 мм. Пошук від −62 до +62 мм дає 15 локально стійких тривимірних положень для окремої частинки радіусом 0,30 мм і густиною 30 кг/м³. Маса кожної частинки — 3,393 мкг. Незалежне заповнення всіх положень дало б сумарно 50,894 мкг; у цьому розрахунку незалежних частинок розсіювання між ними не враховано.

Обидві версії фізики містять виведення від основ акустики, всі графіки результатів, повну таблицю осьових рівноваг і пояснення різниці між масою частинки, запасом сили та межею розміру в моделі.

## Розділи проєкту

| Тема | English | Українська |
|---|---|---|
| Фізика та всі графіки | [Physics and results](docs/physics.md) | [Фізика та результати](docs/physics.uk.md) |
| Конструкція | [Mechanical design](mechanical/README.md) | [Механічна модель](mechanical/README.uk.md) |
| Схема | [Electronics and BOM notation](hardware/README.md) | [Електроніка та позначення BOM](hardware/README.uk.md) |
| Контролер | [Arduino Uno firmware](firmware/README.md) | [Прошивка Arduino Uno](firmware/README.uk.md) |
| Розрахунок | [Numerical model](simulation/README.md) | [Чисельна модель](simulation/README.uk.md) |
| Вихідні дані | [Calculation outputs](results/README.md) | [Результати розрахунків](results/README.uk.md) |
| Програмні засоби | [Software used](tools/README.md) | [Використане ПЗ](tools/README.uk.md) |

## Вихідні файли та дані

| Група | Прямі посилання |
|---|---|
| CAD | [OpenSCAD](mechanical/levitator_frame.scad), [design.json](mechanical/design.json), [generated geometry](mechanical/generated_geometry.scad) |
| STL | [cup](results/concave_cup.stl), [frame](results/support_frame.stl), [assembly](results/levitator_frame.stl), [socket coupon](results/socket_fit_coupon.stl), [viewer](results/view_export.scad) |
| Електроніка | [BOM](hardware/BOM.csv), [connections](hardware/netlist.csv), [diagram](hardware/block_diagram.svg), [SPICE](hardware/driver_tb6612.cir), [model parameters](hardware/generated_driver_params.inc) |
| Arduino | [acoustic_levitator.ino](firmware/acoustic_levitator/acoustic_levitator.ino) |
| Python | [field and force](simulation/acoustic_model.py), [geometry](simulation/array_geometry.py), [simulation](simulation/run_simulation.py), [trap analysis](simulation/trap_analysis.py), [electrical sweep](simulation/run_driver_sweep.py), [electrical plots](simulation/plot_driver.py) |
| Акустичні дані | [geometry](results/array_geometry.csv), [frequency comparison](results/model_summary.csv), [all axial equilibria](results/axial_traps.csv), [capacity calculation](results/capacity_summary.json), [assumptions](results/simulation_metadata.json) |
| Електричні дані | [waveforms](results/driver_waveforms.csv), [sensitivity study](results/driver_sweep.csv) |
| Перевірки | [tests](tests), [mesh analysis](results/mesh_validation.json), [mesh checker](tools/check_meshes.py), [result checker](tools/check_results.py) |

## Графіки

[Осьова сила й потенціал](results/standing_wave_field.png) · [Карти поля](results/array_field_2d.png) · [Фаза](results/phase_sensitivity.png) · [Відстань і частота](results/frequency_separation_map.png) · [Поперечне утримання](results/lateral_stability.png) · [Вертикальні положення](results/vertical_capacity.png) · [Електрична характеристика](results/driver_response.png)

## Джерела

Розділ фізики використовує наведені нижче номери джерел.

1. Marzo, Barnes & Drinkwater, *TinyLev: A multi-emitter single-axis acoustic levitator* (2017). [Стаття](https://doi.org/10.1063/1.4989995).
2. Gor’kov, *Forces acting on a small particle in an acoustic field within an ideal fluid* (1961). [Оригінальна праця](https://www.mathnet.ru/eng/dan25473).
3. Bruus, *Acoustofluidics 7: The acoustic radiation force on small particles* (2012). [Сторінка автора в університетському архіві](https://orbit.dtu.dk/en/publications/acoustofluidics-7-the-acoustic-radiation-force-on-small-particles/).
4. ElecFreaks, *HC-SR04 ultrasonic ranging module*. [Специфікація](https://content.arduino.cc/assets/HCSR04.pdf).
5. Toshiba, *TB6612FNG*. [Специфікація](https://toshiba.semicon-storage.com/info/datasheet_en_20141001.pdf?did=10660).

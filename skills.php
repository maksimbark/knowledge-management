<?PHP

$servername = "<>";
$username = "<>";
$password = "<>";
$dbname = "<>";

$conn = mysqli_connect($servername, $username, $password, $dbname) or die("Connection failed: " . mysqli_connect_error());

/* check connection */
if (mysqli_connect_errno()) {
    printf("Connect failed: %s\n", mysqli_connect_error());
    exit();
}

$sql = "SELECT * FROM `SKILL` ";
$res = mysqli_query($conn, $sql) or die("database error:" . mysqli_error($conn));

$skills_map = [];
$skills_names = [];
$root_ids = [];

while ($row = mysqli_fetch_assoc($res)) {

    if (isset($row['PARENT'])) {
        if (isset($skills_map[$row['PARENT']])) {
            array_push($skills_map[$row['PARENT']], $row['ID']);
        } else {
            $skills_map[$row['PARENT']] = [$row['ID']];
        }
    } else {
        array_push($root_ids, $row['ID']);
    }
    $skills_names[$row['ID']] = $row['NAME_RU'];

}

function get_all_child_ids($skills_map, $id)
{
    $answer = [];
    if (isset($skills_map[$id])) {
        foreach ($skills_map[$id] as $skill) {
            array_push($answer, $skill);
            $answer = array_merge($answer, get_all_child_ids($skills_map, $skill));
        }
    }
    return $answer;
}

function get_all_experts_with_skills_by_ids($conn, $ids)
{
    $sql = "
	select count(owner) as count from (
	SELECT DISTINCT owner
	FROM `COMPETENCY`
	WHERE SKILL in (" . join(", ", $ids) . ")) as k";

    $res = mysqli_query($conn, $sql) or die("database error:" . mysqli_error($conn));
    $row = mysqli_fetch_assoc($res);
    return $row['count'];
}

// для вывода в консоли
/*
foreach($root_ids as $rootid) {
	echo 'rootid '.$rootid.' '.$skills_names[$rootid].': '.PHP_EOL;
	foreach($skills_map[$rootid] as $main_root_child) {
		echo '    mainrootchildid '.$main_root_child.' '.$skills_names[$main_root_child].': ';
		$ids = get_all_child_ids($skills_map, $main_root_child);	
		echo get_all_experts_with_skills_by_ids($conn, $ids).PHP_EOL;
	}
}
*/

?>

<html>
<head>
    <meta charset="utf-8">
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
        google.charts.load('current', {packages: ['corechart', 'bar']});
        google.charts.setOnLoadCallback(drawMaterial);

        function drawMaterial() {
            var data = new google.visualization.DataTable();
            data.addColumn('string', 'Компетенция');
            data.addColumn('number', 'Количество экспертов');

            data.addRows([

                    <?PHP
                    foreach ($root_ids as $rootid) {
                        foreach ($skills_map[$rootid] as $main_root_child) {
                            $ids = get_all_child_ids($skills_map, $main_root_child);
                            echo "[{v:'" . $skills_names[$main_root_child] . "'}, " . get_all_experts_with_skills_by_ids($conn, $ids) . "]," . PHP_EOL;
                        }
                    }
                    ?>
                ]
            );

            var options = {
                hAxis: {
                    textStyle: {
                        fontSize: 12
                    },
                    slantedText: true,
                    slantedTextAngle: 90

                },
            };

            var materialChart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
            materialChart.draw(data, options);
        }
    </script>
</head>
<body>
<div id="chart_div" style="width: 100%; height: 100%;"></div>
</body>
</html>

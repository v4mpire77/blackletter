param(
    [Parameter(Mandatory=$true)][string]$Findings,
    [Parameter(Mandatory=$true)][string]$Out
)

$findings = Get-Content $Findings | ConvertFrom-Json

$html = @"
<html>
<head>
  <meta charset='UTF-8'>
  <title>Compliance Findings</title>
  <style>
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ccc; padding: 4px; vertical-align: top; }
    pre { white-space: pre-wrap; }
  </style>
</head>
<body>
<h1>Compliance Findings</h1>
<table>
  <tr><th>Rule</th><th>Evidence</th><th>Metadata</th></tr>
"@

foreach ($f in $findings) {
    $meta = $f.metadata
    $metaHtml = "<ul>" +
        "<li>Rule Version: $($meta.rule_version)</li>" +
        "<li>Ruleset Hash: $($meta.ruleset_hash)</li>" +
        "<li>Engine Version: $($meta.engine_version)</li>" +
        "<li>Source: $($meta.source_file) p$($meta.page)</li>" +
        (if ($meta.section) { "<li>Section: $($meta.section)</li>" } else { "" }) +
        "<li>Timestamp: $($meta.timestamp)</li>" +
        "</ul>"
    $html += "<tr><td>$($f.rule_text)</td><td><pre>$($f.evidence_snippet)</pre></td><td>$metaHtml</td></tr>"
}

$html += "</table></body></html>"

Set-Content -Path $Out -Value $html
Write-Host "Report written to $Out"

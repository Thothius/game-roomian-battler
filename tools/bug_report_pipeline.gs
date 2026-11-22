/**
 * GungeonMate bug-report pipeline — Google Apps Script.
 *
 * SETUP (one-time, ~10 min, all free):
 *
 * 1. Create a Google Sheet (e.g. "GungeonMate Bug Reports") with columns:
 *      A: received_at   B: kind   C: screen   D: entity
 *      E: app_version   F: platform   G: notes   H: status   I: fixed_in
 *
 * 2. Go to https://script.google.com → New project → paste this file → Save.
 *
 * 3. Project Settings (gear icon) → Script Properties → add:
 *      SHEET_ID = the spreadsheet ID from its URL
 *        (https://docs.google.com/spreadsheets/d/<THIS_PART>/edit)
 *
 * 4. Run `installTrigger` once from the editor (authorizes + creates the
 *    1-minute inbox trigger). Or Deploy → New deployment → Web app is NOT
 *    needed; the time trigger does everything.
 *
 * 5. In Gmail: create label "bug-reports", then Settings → Filters →
 *    from:faaremets.fristjan@gmail.com OR subject:"GM-BUG" → apply label.
 *    (Reports arrive at that inbox; the trigger scans the label.)
 *
 * The script parses subjects like:
 *   GM-BUG v3.7.0|Bug|Item Detail|Hegemony
 * and appends rows to the sheet. Duplicate subject+notes within 24h are
 * skipped so retries don't double-log.
 */

const LABEL_NAME = 'bug-reports';
const SUBJECT_PREFIX = 'GM-BUG';
const LOOKBACK_MINUTES = 10; // trigger runs every 1 min; overlap is safe (dedupe below)
const DEDUPE_HOURS = 24;

function installTrigger() {
  // Remove any existing trigger first so re-running is idempotent.
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'processBugReports') {
      ScriptApp.deleteTrigger(t);
    }
  });
  ScriptApp.newTrigger('processBugReports')
    .timeBased()
    .everyMinutes(1)
    .create();
}

function processBugReports() {
  const sheet = getSheet_();
  const threads = GmailApp.search(
    'label:' + LABEL_NAME + ' newer_than:' + LOOKBACK_MINUTES + 'm',
    0,
    50
  );

  threads.forEach(function (thread) {
    thread.getMessages().forEach(function (msg) {
      // The label+search already scopes to the report inbox; ingest
      // anything with a GM-BUG subject (ingestMessage_ re-checks).
      ingestMessage_(sheet, msg);
    });
  });
}

function ingestMessage_(sheet, msg) {
  const subject = msg.getSubject() || '';
  if (subject.indexOf(SUBJECT_PREFIX) !== 0) return;

  const parts = subject.split('|').map(function (s) { return s.trim(); });
  // parts: [GM-BUG vX.Y.Z, Kind, Screen, Entity?]
  const version = (parts[0] || '').replace(/^GM-BUG\s*v?/, '');
  const kind = parts[1] || '';
  const screen = parts[2] || '';
  const entity = parts.length > 3 ? parts.slice(3).join('|') : '';

  const body = msg.getPlainBody() || '';
  const notes = body.split('\n---\n')[0].trim();
  const meta = parseMeta_(body);

  // Dedupe: same screen+entity+notes within DEDUPE_HOURS → skip.
  const lastRow = sheet.getLastRow();
  if (lastRow > 1) {
    const recent = sheet.getRange(2, 1, lastRow - 1, 9).getValues();
    const cutoff = new Date(Date.now() - DEDUPE_HOURS * 3600 * 1000);
    for (let i = recent.length - 1; i >= 0; i--) {
      const r = recent[i];
      const when = r[0] instanceof Date ? r[0] : new Date(r[0]);
      if (when < cutoff) break; // sheet is append-ordered
      if (r[2] === screen && (r[3] || '') === entity && r[6] === notes) {
        return; // duplicate
      }
    }
  }

  sheet.appendRow([
    msg.getDate(),
    kind,
    screen,
    entity,
    version || meta.APP || '',
    meta.PLATFORM || '',
    notes,
    'NEW',
    '',
  ]);
}

function parseMeta_(body) {
  const meta = {};
  const lines = body.split('\n');
  let inBlock = false;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].trim() === '---') { inBlock = true; continue; }
    if (inBlock) {
      const m = lines[i].match(/^([A-Z_]+):\s*(.*)$/);
      if (m) meta[m[1]] = m[2].trim();
    }
  }
  return meta;
}

function getSheet_() {
  const props = PropertiesService.getScriptProperties();
  const id = props.getProperty('SHEET_ID');
  if (!id) throw new Error('Set SHEET_ID script property first.');
  return SpreadsheetApp.openById(id).getActiveSheet();
}

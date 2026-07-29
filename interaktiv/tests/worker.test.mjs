import assert from 'node:assert/strict';
import { test } from 'node:test';
import { createWorker } from '../server/runtime.js';

const assets = new Map([
  ['/', { body: '<!doctype html><title>Labor</title>', contentType: 'text/html; charset=utf-8' }]
]);

function environment(overrides = {}) {
  return {
    OPENAI_API_KEY: 'server-secret',
    AI_SAFETY_SALT: 'test-salt-with-at-least-32-characters',
    AI_RATE_LIMITER: {
      async limit() {
        return { success: true };
      }
    },
    ...overrides
  };
}

function apiRequest(body, options = {}) {
  return new Request('https://anschlusslabor.test/api/anschluss', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Origin: 'https://anschlusslabor.test',
      'CF-Connecting-IP': '203.0.113.8',
      ...options.headers
    },
    body: JSON.stringify(body)
  });
}

test('Der KI-Endpunkt bleibt ohne serverseitige Schutzkonfiguration deaktiviert', async () => {
  const originalFetch = globalThis.fetch;
  let calls = 0;
  globalThis.fetch = async () => {
    calls += 1;
    throw new Error('must not be called');
  };
  try {
    const response = await createWorker(assets).fetch(apiRequest({
      move: 'fortsetzen',
      previousText: 'Ausgang.'
    }), {});
    assert.equal(response.status, 503);
    assert.equal(calls, 0);
    assert.match((await response.json()).error, /nicht eingerichtet/);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test('Der Worker sendet nur validierte Minimaldaten und ein anonymisiertes Safety-Kennzeichen', async () => {
  const originalFetch = globalThis.fetch;
  let upstreamRequest;
  globalThis.fetch = async (url, options) => {
    upstreamRequest = { url, options };
    return new Response(JSON.stringify({
      status: 'completed',
      output: [{
        type: 'message',
        content: [{
          type: 'output_text',
          text: JSON.stringify({
            suggestion: 'Eine begrenzte Fortsetzung.',
            explanation: 'Sie könnte den bezeichneten Zusammenhang weiterführen.'
          })
        }]
      }]
    }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  };

  try {
    const response = await createWorker(assets).fetch(apiRequest({
      move: 'fortsetzen',
      previousText: 'Der Ausgang ist bedingt.'
    }), environment());
    assert.equal(response.status, 200);
    assert.equal(response.headers.get('Cache-Control'), 'no-store');
    assert.deepEqual(await response.json(), {
      suggestion: 'Eine begrenzte Fortsetzung.',
      explanation: 'Sie könnte den bezeichneten Zusammenhang weiterführen.'
    });

    assert.equal(upstreamRequest.url, 'https://api.openai.com/v1/responses');
    assert.equal(upstreamRequest.options.headers.Authorization, 'Bearer server-secret');
    const upstreamBody = JSON.parse(upstreamRequest.options.body);
    assert.equal(upstreamBody.model, 'gpt-5.6-sol');
    assert.equal(upstreamBody.store, false);
    assert.equal(upstreamBody.reasoning.effort, 'low');
    assert.equal(upstreamBody.text.format.type, 'json_schema');
    assert.equal(upstreamBody.text.format.strict, true);
    assert.notEqual(upstreamBody.safety_identifier, '203.0.113.8');
    assert.equal(upstreamBody.safety_identifier.length, 64);
    assert.doesNotMatch(upstreamRequest.options.body, /versions/);
    assert.doesNotMatch(upstreamRequest.options.body, /server-secret/);
    assert.match(upstreamRequest.options.body, /Der Ausgang ist bedingt/);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test('Ungültige, fremde und gedrosselte Anfragen erreichen OpenAI nicht', async () => {
  const originalFetch = globalThis.fetch;
  let calls = 0;
  globalThis.fetch = async () => {
    calls += 1;
    throw new Error('must not be called');
  };
  const worker = createWorker(assets);

  try {
    const invalid = await worker.fetch(apiRequest({
      move: 'beliebig',
      previousText: 'Ausgang.'
    }), environment());
    assert.equal(invalid.status, 400);

    const extraData = await worker.fetch(apiRequest({
      move: 'fortsetzen',
      previousText: 'Ausgang.',
      versions: ['nicht autorisiert']
    }), environment());
    assert.equal(extraData.status, 400);

    const foreign = await worker.fetch(apiRequest({
      move: 'fortsetzen',
      previousText: 'Ausgang.'
    }, { headers: { Origin: 'https://fremd.test' } }), environment());
    assert.equal(foreign.status, 403);

    const missingOrigin = await worker.fetch(apiRequest({
      move: 'fortsetzen',
      previousText: 'Ausgang.'
    }, { headers: { Origin: '' } }), environment());
    assert.equal(missingOrigin.status, 403);

    const wrongMediaType = await worker.fetch(apiRequest({
      move: 'fortsetzen',
      previousText: 'Ausgang.'
    }, { headers: { 'Content-Type': 'application/jsonp' } }), environment());
    assert.equal(wrongMediaType.status, 415);

    const oversized = await worker.fetch(apiRequest({
      move: 'fortsetzen',
      previousText: 'x'.repeat(2_100)
    }), environment());
    assert.equal(oversized.status, 413);

    const missingIdentifier = await worker.fetch(apiRequest({
      move: 'fortsetzen',
      previousText: 'Ausgang.'
    }, { headers: { 'CF-Connecting-IP': '' } }), environment());
    assert.equal(missingIdentifier.status, 400);

    const limited = await worker.fetch(apiRequest({
      move: 'fortsetzen',
      previousText: 'Ausgang.'
    }), environment({
      AI_RATE_LIMITER: {
        async limit() {
          return { success: false };
        }
      }
    }));
    assert.equal(limited.status, 429);
    assert.equal(limited.headers.get('Retry-After'), '60');

    const limiterFailure = await worker.fetch(apiRequest({
      move: 'fortsetzen',
      previousText: 'Ausgang.'
    }), environment({
      AI_RATE_LIMITER: {
        async limit() {
          throw new Error('binding unavailable');
        }
      }
    }));
    assert.equal(limiterFailure.status, 503);
    assert.equal(calls, 0);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test('Statische Assets erlauben nur GET und HEAD und setzen eine restriktive CSP', async () => {
  const worker = createWorker(assets);
  const getResponse = await worker.fetch(new Request('https://anschlusslabor.test/'), {});
  assert.equal(getResponse.status, 200);
  assert.match(getResponse.headers.get('Content-Security-Policy'), /connect-src 'self'/);
  assert.match(getResponse.headers.get('Content-Security-Policy'), /object-src 'none'/);

  const postResponse = await worker.fetch(new Request('https://anschlusslabor.test/', { method: 'POST' }), {});
  assert.equal(postResponse.status, 405);
});

test('Verweigerte, unvollständige und ungültige Modellausgaben werden nicht durchgereicht', async () => {
  const originalFetch = globalThis.fetch;
  const results = [
    { status: 'completed', output: [{ content: [{ type: 'refusal', refusal: 'Nein' }] }] },
    { status: 'incomplete', output: [] },
    { status: 'completed', output_text: '{"suggestion":"","explanation":"leer"}' }
  ];
  globalThis.fetch = async () => new Response(JSON.stringify(results.shift()), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  });

  try {
    for (let index = 0; index < 3; index += 1) {
      const response = await createWorker(assets).fetch(apiRequest({
        move: 'praezisieren',
        previousText: 'Ein begrenzter Bezug.'
      }), environment());
      assert.equal(response.status, 502);
      const body = await response.json();
      assert.deepEqual(Object.keys(body), ['error']);
      assert.doesNotMatch(body.error, /Nein|incomplete|invalid-output/);
    }
  } finally {
    globalThis.fetch = originalFetch;
  }
});

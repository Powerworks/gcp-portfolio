---
title: "K9 Crush"
subtitle: "E-Commerce or Platform Subsystem"
category: "AI" # Or "Backend", depending on how you want to filter it
order: 2
tech: ["Vue.js", "Tailwind CSS", "Node.js"]
repoUrl: "https://github.com/yourusername/k9crush" # Optional: remove this line if there's no public repo
---

# K9 Crush Project Overview
### Architectural Decision Record (ADR)
* **Problem:** Managing cross-module event distribution cleanly without creating tight internal coupling or complex local pub/sub overhead.
* **Alternatives Considered:** In-memory mediator patterns vs. isolated transport infrastructure.
* **Decision:** Route same-module event cascades directly through the shared `k9crush.events` RabbitMQ exchange rather than a separate local pub/sub mechanism.
* **Verification:** Source-verified against Wolverine's transport behavior (default fanout exchange, graceful no-op acknowledgment for modules without a local handler).
* **Explicit Revisit Trigger:** System performance degradation under high-throughput event cascades or scale constraints requiring modular separation to independent microservices.

### Implementation Snippet
```csharp
// Example configuration of the Wolverine exchange cascade verified against transport source
public static IHostBuilder ConfigureMessaging(this IHostBuilder builder)
{
    builder.UseWolverine(opts =>
    {
        opts.PublishAllMessages().ToRabbitExchange("k9crush.events", exchange =>
        {
            exchange.ExchangeType = "fanout";
            exchange.BindQueue("k9crush.local.queue");
        });
    });
    return builder;
}
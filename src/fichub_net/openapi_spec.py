from typing import Any


def build_openapi_spec(server_url: str) -> dict[str, Any]:
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "FicHub API",
            "version": "0.1.0",
            "description": (
                "Public endpoints for exporting and retrieving fanfiction metadata. "
                "Please set a custom User-Agent, avoid concurrent burst traffic, "
                "and handle 429 responses with Retry-After."
            ),
        },
        "servers": [{"url": server_url, "description": "Current server"}],
        "paths": {
            "/api/v0/epub": {
                "get": {
                    "summary": "Export a fic and return download URLs",
                    "parameters": [
                        {
                            "name": "q",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "string"},
                            "description": "Full source URL of the fic",
                        },
                        {
                            "name": "id",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string"},
                            "description": "Optional known FicHub url id",
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "Export metadata and generated URLs",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/EpubSuccessResponse"
                                    }
                                }
                            },
                        },
                        "429": {
                            "description": "Too many requests",
                            "headers": {
                                "Retry-After": {
                                    "description": "Seconds to wait before retry",
                                    "schema": {"type": "string"},
                                }
                            },
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/RateLimitedResponse"
                                    }
                                }
                            },
                        },
                        "4XX": {
                            "description": "Client error (for example missing/invalid parameters or forbidden source)",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/EpubErrorResponse"
                                    }
                                }
                            },
                        },
                        "5XX": {
                            "description": "Server or upstream failure",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/EpubErrorResponse"
                                    }
                                }
                            },
                        },
                    },
                }
            },
            "/api/v0/meta": {
                "get": {
                    "summary": "Get parsed metadata for a fic",
                    "parameters": [
                        {
                            "name": "q",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "string"},
                            "description": "Full source URL of the fic",
                        },
                        {
                            "name": "id",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string"},
                            "description": "Optional known FicHub url id",
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "Metadata for fic",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/FicMetadata"
                                    }
                                }
                            },
                        },
                        "429": {
                            "description": "Too many requests",
                            "headers": {
                                "Retry-After": {
                                    "description": "Seconds to wait before retry",
                                    "schema": {"type": "string"},
                                }
                            },
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/RateLimitedResponse"
                                    }
                                }
                            },
                        },
                        "4XX": {
                            "description": "Client error (for example missing/invalid parameters or forbidden source)",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/EpubErrorResponse"
                                    }
                                }
                            },
                        },
                        "5XX": {
                            "description": "Server or upstream failure",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/EpubErrorResponse"
                                    }
                                }
                            },
                        },
                    },
                }
            },
            "/api/v0/remote": {
                "get": {
                    "summary": "Return request source context",
                    "responses": {
                        "200": {
                            "description": "Source context for current request",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/RemoteSourceResponse"
                                    }
                                }
                            },
                        }
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "RateLimitedResponse": {
                    "type": "object",
                    "properties": {
                        "err": {"type": "integer", "example": -429},
                        "msg": {"type": "string", "example": "too many requests"},
                        "retry_after": {"type": "integer", "example": 8},
                    },
                    "required": ["err", "msg", "retry_after"],
                    "additionalProperties": True,
                },
                "EpubErrorResponse": {
                    "type": "object",
                    "properties": {
                        "err": {
                            "type": "integer",
                            "description": "Internal error code",
                        },
                        "msg": {
                            "type": "string",
                            "description": "Human-readable error summary",
                        },
                        "q": {"type": "string", "description": "Query URL/value"},
                        "fixits": {
                            "type": "array",
                            "description": "Suggested corrections or alternatives",
                            "items": {"type": "string"},
                        },
                        "key": {
                            "type": "string",
                            "description": "Missing expected key (ensure_failed)",
                        },
                        "etext": {
                            "type": ["string", "null"],
                            "description": "Backend/exporter error text",
                        },
                        "res": {
                            "type": "string",
                            "description": "Detailed upstream parsing or resolution info",
                        },
                        "ret": {
                            "type": "integer",
                            "description": "Upstream return code",
                        },
                        "upstream": {
                            "type": "boolean",
                            "description": "Whether failure originated from upstream service",
                        },
                        "meta": {"$ref": "#/components/schemas/FicMetadata"},
                        "retry_after": {"type": "integer"},
                    },
                    "required": ["err", "msg"],
                    "additionalProperties": True,
                },
                "RemoteSourceResponse": {
                    "type": "object",
                    "properties": {
                        "created": {"type": "string", "format": "date-time"},
                        "description": {"type": "string"},
                        "id": {"type": "integer"},
                        "is_automated": {"type": "boolean"},
                        "route": {"type": "string", "format": "uri"},
                    },
                    "required": [
                        "created",
                        "description",
                        "id",
                        "is_automated",
                        "route",
                    ],
                    "additionalProperties": True,
                },
                "EpubSuccessResponse": {
                    "type": "object",
                    "properties": {
                        "q": {"type": "string"},
                        "err": {"type": "integer", "example": 0},
                        "fixits": {"type": "array", "items": {"type": "string"}},
                        "info": {"type": "string"},
                        "urlId": {"type": "string"},
                        "slug": {"type": "string"},
                        "epub_url": {"type": "string"},
                        "html_url": {"type": "string"},
                        "mobi_url": {"type": "string"},
                        "pdf_url": {"type": "string"},
                        "hashes": {
                            "type": "object",
                            "additionalProperties": {"type": "string"},
                        },
                        "notes": {"type": "array", "items": {"type": "string"}},
                        "meta": {"$ref": "#/components/schemas/FicMetadata"},
                        "urls": {
                            "type": "object",
                            "additionalProperties": {"type": "string"},
                        },
                    },
                    "required": [
                        "err",
                        "q",
                        "fixits",
                        "info",
                        "urlId",
                        "urls",
                        "epub_url",
                    ],
                    "additionalProperties": True,
                },
                "FicMetadata": {
                    "type": "object",
                    "properties": {
                        "author": {"type": "string"},
                        "authorId": {"type": ["integer", "null"]},
                        "authorLocalId": {"type": ["string", "null"]},
                        "authorUrl": {"type": ["string", "null"]},
                        "chapters": {"type": "integer"},
                        "created": {"type": "string", "format": "date-time"},
                        "description": {"type": "string"},
                        "extraMeta": {"type": ["string", "null"]},
                        "id": {"type": "string"},
                        "rawExtendedMeta": {
                            "oneOf": [
                                {"type": "null"},
                                {
                                    "$ref": "#/components/schemas/FicHubRawExtendedMetaFFN"
                                },
                                {
                                    "$ref": "#/components/schemas/FicHubRawExtendedMetaAO3"
                                },
                            ]
                        },
                        "source": {"type": "string"},
                        "sourceId": {"type": ["integer", "null"]},
                        "status": {"type": "string"},
                        "title": {"type": "string"},
                        "updated": {"type": "string", "format": "date-time"},
                        "words": {"type": "integer"},
                    },
                    "required": [
                        "author",
                        "authorId",
                        "authorLocalId",
                        "authorUrl",
                        "chapters",
                        "created",
                        "description",
                        "id",
                        "source",
                        "sourceId",
                        "status",
                        "title",
                        "updated",
                        "words",
                    ],
                    "additionalProperties": True,
                },
                "FicHubRawExtendedMetaFFN": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string"},
                        "chapters": {"type": "string"},
                        "characters": {"type": "string"},
                        "crossover": {"type": "boolean"},
                        "fandom_stubs": {"type": "array", "items": {"type": "string"}},
                        "favorites": {"type": "string"},
                        "follows": {"type": "string"},
                        "id": {"type": "string"},
                        "language": {"type": "string"},
                        "published": {"type": "string"},
                        "rated": {"type": "string"},
                        "raw_fandom": {"type": "string"},
                        "reviews": {"type": "string"},
                        "status": {"type": "string"},
                        "updated": {"type": "string"},
                        "words": {"type": "string"},
                    },
                    "required": [
                        "category",
                        "chapters",
                        "characters",
                        "crossover",
                        "fandom_stubs",
                        "favorites",
                        "follows",
                        "id",
                        "language",
                        "published",
                        "rated",
                        "raw_fandom",
                        "reviews",
                        "status",
                        "updated",
                        "words",
                    ],
                    "additionalProperties": True,
                },
                "FicHubRawExtendedMetaAO3": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "array", "items": {"type": "string"}},
                        "category_hrefs": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "character": {"type": "array", "items": {"type": "string"}},
                        "character_hrefs": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "fandom": {"type": "array", "items": {"type": "string"}},
                        "fandom_hrefs": {"type": "array", "items": {"type": "string"}},
                        "freeform": {"type": "array", "items": {"type": "string"}},
                        "freeform_hrefs": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "language": {"type": "string"},
                        "rating": {"type": "array", "items": {"type": "string"}},
                        "rating_hrefs": {"type": "array", "items": {"type": "string"}},
                        "relationship": {"type": "array", "items": {"type": "string"}},
                        "relationship_hrefs": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "series": {"type": "array", "items": {"type": "string"}},
                        "series_hrefs": {"type": "array", "items": {"type": "string"}},
                        "stats": {
                            "type": "object",
                            "properties": {
                                "bookmarks": {"type": "string"},
                                "chapters": {"type": "string"},
                                "comments": {"type": "string"},
                                "hits": {"type": "string"},
                                "kudos": {"type": "string"},
                                "published": {"type": "string", "format": "date-time"},
                                "status": {"type": "string", "format": "date-time"},
                                "words": {"type": "string"},
                            },
                            "required": [
                                "bookmarks",
                                "chapters",
                                "comments",
                                "hits",
                                "kudos",
                                "published",
                                "status",
                                "words",
                            ],
                            "additionalProperties": True,
                        },
                        "warning": {"type": "array", "items": {"type": "string"}},
                        "warning_hrefs": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": [
                        "category",
                        "category_hrefs",
                        "character",
                        "character_hrefs",
                        "fandom",
                        "fandom_hrefs",
                        "freeform",
                        "freeform_hrefs",
                        "language",
                        "rating",
                        "rating_hrefs",
                        "relationship",
                        "relationship_hrefs",
                        "stats",
                        "warning",
                        "warning_hrefs",
                    ],
                    "additionalProperties": True,
                },
            }
        },
    }

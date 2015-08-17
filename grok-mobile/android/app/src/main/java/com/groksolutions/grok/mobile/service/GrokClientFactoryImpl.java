/*
 * Numenta Platform for Intelligent Computing (NuPIC)
 * Copyright (C) 2015, Numenta, Inc.  Unless you have purchased from
 * Numenta, Inc. a separate commercial license for this software code, the
 * following terms and conditions apply:
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero Public License version 3 as
 * published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU Affero Public License for more details.
 *
 * You should have received a copy of the GNU Affero Public License
 * along with this program.  If not, see http://www.gnu.org/licenses.
 *
 * http://numenta.org/licenses/
 *
 */

package com.groksolutions.grok.mobile.service;

import com.numenta.core.service.GrokClient;
import com.numenta.core.service.GrokClientFactory;

import java.net.MalformedURLException;

/**
 * Default factory used to create {@link com.numenta.core.service.GrokClient}
 */
public class GrokClientFactoryImpl implements GrokClientFactory {

    @Override
    public GrokClient createClient(String serverUrl, String pass) throws MalformedURLException {
        return new GrokClientImpl(serverUrl, pass);
    }

}
